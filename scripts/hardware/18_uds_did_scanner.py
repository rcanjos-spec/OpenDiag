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

TX_ID = 0x18DA10F1
RX_ID = 0x18DAF110
FLOW_CONTROL_ID = 0x18DA10F1

DIDS_TO_SCAN = [
    0xF18A,
    0xF18B,
    0xF18C,
    0xF18D,
    0xF18E,
    0xF190,  # controle positivo
    0xF191,
    0xF192,
    0xF193,
    0xF194,
    0xF195,
    0xF196,
    0xF197,
    0xF198,
    0xF199,
]

LOG_DIR = Path("logs/dids")


def main() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    bus = PythonCANBus(
        interface="slcan",
        channel="COM6",
        bitrate=500000,
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

    results = []

    print("## KACTOENG - UDS DID Scanner")
    print()
    print("Interface : COM6")
    print("Bitrate   : 500000")
    print(f"TX ID     : {TX_ID:08X}")
    print(f"RX ID     : {RX_ID:08X}")
    print(f"FC ID     : {FLOW_CONTROL_ID:08X}")
    print()
    print("DIDs selecionados:")
    print(" ".join(f"0x{did:04X}" for did in DIDS_TO_SCAN))
    print()

    try:
        for did in DIDS_TO_SCAN:
            print(
                f"Consultando DID 0x{did:04X}...",
                end=" ",
                flush=True,
            )

            started = time.monotonic()

            try:
                response = client.read_data_by_identifier(did)

                elapsed = time.monotonic() - started

                if isinstance(response, NegativeResponse):
                    result = {
                        "did": f"0x{did:04X}",
                        "status": "negative",
                        "original_sid": (f"0x{response.original_sid:02X}"),
                        "response_code": (f"0x{response.response_code:02X}"),
                        "elapsed_ms": round(
                            elapsed * 1000,
                            2,
                        ),
                    }

                    results.append(result)

                    print(f"NEGATIVO | NRC=0x{response.response_code:02X}")

                    continue

                result = {
                    "did": f"0x{did:04X}",
                    "status": "positive",
                    "response_did": (f"0x{response.did:04X}"),
                    "length": len(response.value),
                    "data": response.value.hex(" ").upper(),
                    "elapsed_ms": round(
                        elapsed * 1000,
                        2,
                    ),
                }

                results.append(result)

                print(
                    "OK | "
                    f"{len(response.value)} bytes | "
                    f"{response.value.hex(' ').upper()}"
                )

            except (TimeoutError, ValueError) as exc:
                elapsed = time.monotonic() - started

                result = {
                    "did": f"0x{did:04X}",
                    "status": "error",
                    "error": type(exc).__name__,
                    "message": str(exc),
                    "elapsed_ms": round(
                        elapsed * 1000,
                        2,
                    ),
                }

                results.append(result)

                print(f"ERRO | {type(exc).__name__}: {exc}")

    finally:
        bus.shutdown()

    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

    log_path = LOG_DIR / f"did_scan_{timestamp}.json"

    document = {
        "timestamp": datetime.now(UTC).isoformat(),
        "interface": "COM6",
        "bitrate": 500000,
        "tx_id": f"0x{TX_ID:08X}",
        "rx_id": f"0x{RX_ID:08X}",
        "flow_control_id": (f"0x{FLOW_CONTROL_ID:08X}"),
        "dids": [f"0x{did:04X}" for did in DIDS_TO_SCAN],
        "results": results,
    }

    log_path.write_text(
        json.dumps(
            document,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    positive = sum(1 for result in results if result["status"] == "positive")

    negative = sum(1 for result in results if result["status"] == "negative")

    errors = sum(1 for result in results if result["status"] == "error")

    print()
    print("================================")
    print("Scanner finalizado")
    print(f"DIDs positivos : {positive}")
    print(f"DIDs negativos : {negative}")
    print(f"Erros          : {errors}")
    print(f"Total          : {len(results)}")
    print(f"Log            : {log_path}")
    print("================================")


if __name__ == "__main__":
    main()
