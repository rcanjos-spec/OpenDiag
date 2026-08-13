import json
import time
from datetime import UTC, datetime
from pathlib import Path

from opendiag.bus.python_can import PythonCANBus
from opendiag.protocols.isotp_transport import ISOTPTransport
from opendiag.uds.client import UDSClient
from opendiag.uds.response import NegativeResponse
from opendiag.uds.response_parser import UDSResponseParser
from opendiag.uds.response_registry import ResponseRegistry

# ============================================================
# KACTOENG - UDS Variable DID Scanner
# ECU: Magneti Marelli IAW 10GF
# ============================================================

INTERFACE = "COM6"
BITRATE = 500000

TX_ID = 0x18DA10F1
RX_ID = 0x18DAF110
FLOW_CONTROL_ID = 0x18DA10F1


# Região que será pesquisada
SCAN_START = 0x1000
SCAN_END = 0xA5FF

# Tamanho de cada bloco
BLOCK_SIZE = 0x100

# Diretório dos logs
LOG_DIR = Path("logs/dids")


def scan_block(client: UDSClient, start_did: int, end_did: int) -> dict:
    """
    Varre um bloco de DIDs.

    No terminal:
        - mostra somente positivos
        - não mostra NRC 0x31

    No retorno:
        - positivos
        - quantidade de negativos
        - quantidade de erros
    """

    positives = []
    negative_count = 0
    error_count = 0

    for did in range(start_did, end_did + 1):
        started = time.monotonic()

        try:
            response = client.read_data_by_identifier(did)

            elapsed_ms = round(
                (time.monotonic() - started) * 1000,
                2,
            )

            # ------------------------------------------------
            # Resposta negativa
            # ------------------------------------------------
            if isinstance(response, NegativeResponse):
                negative_count += 1

                # Não imprimir NRC 0x31
                continue

            # ------------------------------------------------
            # Resposta positiva
            # ------------------------------------------------
            raw_data = bytes(response.value)

            result = {
                "did": f"0x{did:04X}",
                "status": "positive",
                "response_did": f"0x{response.did:04X}",
                "length": len(raw_data),
                "data": raw_data.hex(" ").upper(),
                "ascii": raw_data.decode(
                    "ascii",
                    errors="replace",
                ),
                "elapsed_ms": elapsed_ms,
            }

            positives.append(result)

            # Mostrar SOMENTE positivos
            print(
                f"  0x{did:04X} | "
                f"{len(raw_data):02d} bytes | "
                f"{raw_data.hex(' ').upper()}"
            )

        except (TimeoutError, ValueError) as exc:
            error_count += 1

            elapsed_ms = round(
                (time.monotonic() - started) * 1000,
                2,
            )

            # Erros não são considerados DIDs positivos
            # e não interrompem a varredura.
            print(f"  [ERRO] 0x{did:04X} | {type(exc).__name__}: {exc}")

    return {
        "start_did": f"0x{start_did:04X}",
        "end_did": f"0x{end_did:04X}",
        "positive_count": len(positives),
        "negative_count": negative_count,
        "error_count": error_count,
        "positives": positives,
    }


def main() -> None:

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print()
    print("========================================")
    print(" KACTOENG - UDS Variable DID Scanner")
    print(" ECU: Magneti Marelli IAW 10GF")
    print("========================================")
    print()
    print(f"Interface : {INTERFACE}")
    print(f"Bitrate   : {BITRATE}")
    print(f"TX ID     : {TX_ID:08X}")
    print(f"RX ID     : {RX_ID:08X}")
    print(f"FC ID     : {FLOW_CONTROL_ID:08X}")
    print()
    print(f"Faixa     : 0x{SCAN_START:04X}–0x{SCAN_END:04X}")
    print(f"Blocos    : 0x{BLOCK_SIZE:02X} DIDs")
    print()
    print("Somente DIDs positivos serão exibidos.")
    print()

    bus = PythonCANBus(
        interface="slcan",
        channel=INTERFACE,
        bitrate=BITRATE,
    )

    transport = ISOTPTransport(
        bus=bus,
        tx_id=TX_ID,
        tx_extended=True,
        rx_id=RX_ID,
        flow_control_id=FLOW_CONTROL_ID,
        reassembly_timeout=5.0,
    )

    parser = UDSResponseParser(
        registry=ResponseRegistry(),
    )

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    blocks = []

    total_positive = 0
    total_negative = 0
    total_errors = 0

    started_total = time.monotonic()

    try:
        # ====================================================
        # Varredura automática por blocos
        # ====================================================

        for block_start in range(
            SCAN_START,
            SCAN_END + 1,
            BLOCK_SIZE,
        ):
            block_end = min(
                block_start + BLOCK_SIZE - 1,
                SCAN_END,
            )

            print()
            print(f"===== 0x{block_start:04X}–0x{block_end:04X} =====")

            block_result = scan_block(
                client,
                block_start,
                block_end,
            )

            blocks.append(block_result)

            total_positive += block_result["positive_count"]

            total_negative += block_result["negative_count"]

            total_errors += block_result["error_count"]

            print(f"Positivos no bloco: {block_result['positive_count']}")

    finally:
        bus.shutdown()

    elapsed_total = round(
        time.monotonic() - started_total,
        2,
    )

    # ========================================================
    # JSON
    # ========================================================

    timestamp = datetime.now(UTC)

    log_name = f"variable_did_scan_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"

    log_path = LOG_DIR / log_name

    document = {
        "timestamp": timestamp.isoformat(),
        "project": "KACTOENG",
        "ecu": {
            "manufacturer": "Magneti Marelli",
            "model": "IAW 10GF",
        },
        "interface": INTERFACE,
        "bitrate": BITRATE,
        "tx_id": f"0x{TX_ID:08X}",
        "rx_id": f"0x{RX_ID:08X}",
        "flow_control_id": (f"0x{FLOW_CONTROL_ID:08X}"),
        "scan": {
            "start_did": f"0x{SCAN_START:04X}",
            "end_did": f"0x{SCAN_END:04X}",
            "block_size": BLOCK_SIZE,
        },
        "summary": {
            "positive": total_positive,
            "negative": total_negative,
            "errors": total_errors,
            "total": (total_positive + total_negative + total_errors),
            "elapsed_seconds": elapsed_total,
        },
        "blocks": blocks,
    }

    log_path.write_text(
        json.dumps(
            document,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    # ========================================================
    # Resumo final
    # ========================================================

    print()
    print("================================")
    print("Scanner finalizado")
    print(f"DIDs positivos : {total_positive}")
    print(f"DIDs negativos : {total_negative}")
    print(f"Erros          : {total_errors}")
    print(f"Total          : {total_positive + total_negative + total_errors}")
    print(f"Tempo          : {elapsed_total:.2f} s")
    print(f"Log            : {log_path}")
    print("================================")


if __name__ == "__main__":
    main()
