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

LOG_DIR = Path("logs/ecu_data")


KNOWN_DIDS = {
    0xF18C: {
        "name": "ECU Serial Number",
        "type": "ascii",
    },
    0xF190: {
        "name": "Vehicle Identification Number",
        "type": "ascii",
    },
    0xF191: {
        "name": "Vehicle Manufacturer ECU Hardware Number",
        "type": "ascii",
        "status": "value_under_investigation",
    },
    0xF192: {
        "name": "System Supplier ECU Hardware Number",
        "type": "ascii",
    },
    0xF193: {
        "name": "System Supplier ECU Hardware Version",
        "type": "hex",
    },
    0xF194: {
        "name": "System Supplier ECU Software Number",
        "type": "ascii",
    },
    0xF195: {
        "name": "System Supplier ECU Software Version",
        "type": "hex",
    },
    0xF196: {
        "name": "Exhaust Regulation / Type Approval Number",
        "type": "ascii",
    },
}


def decode_value(raw: bytes, value_type: str):
    if value_type == "ascii":
        return raw.decode("ascii", errors="replace").rstrip("\x00")

    return raw.hex(" ").upper()


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

    print("## KACTOENG - UDS ECU Data Reader")
    print()
    print("Interface : COM6")
    print("Bitrate   : 500000")
    print(f"TX ID     : {TX_ID:08X}")
    print(f"RX ID     : {RX_ID:08X}")
    print(f"FC ID     : {FLOW_CONTROL_ID:08X}")
    print()

    try:
        for did, definition in KNOWN_DIDS.items():
            print(
                f"Consultando DID 0x{did:04X} - {definition['name']}...",
                end=" ",
            )

            started = time.monotonic()

            try:
                response = client.read_data_by_identifier(did)

                elapsed = time.monotonic() - started

                if isinstance(response, NegativeResponse):
                    result = {
                        "did": f"0x{did:04X}",
                        "name": definition["name"],
                        "type": definition["type"],
                        "status": "negative",
                        "nrc": f"0x{response.response_code:02X}",
                        "elapsed_ms": round(elapsed * 1000, 2),
                    }

                    results.append(result)

                    print(f"NEGATIVO | NRC=0x{response.response_code:02X}")
                    continue

                raw = bytes(response.value)
                value = decode_value(
                    raw,
                    definition["type"],
                )

                result = {
                    "did": f"0x{did:04X}",
                    "name": definition["name"],
                    "type": definition["type"],
                    "status": definition.get(
                        "status",
                        "positive",
                    ),
                    "raw": raw.hex(" ").upper(),
                    "value": value,
                    "length": len(raw),
                    "elapsed_ms": round(elapsed * 1000, 2),
                }

                results.append(result)

                print(f"OK | {value} | {len(raw)} bytes")

            except (TimeoutError, ValueError) as exc:
                elapsed = time.monotonic() - started

                result = {
                    "did": f"0x{did:04X}",
                    "name": definition["name"],
                    "type": definition["type"],
                    "status": "error",
                    "error": type(exc).__name__,
                    "message": str(exc),
                    "elapsed_ms": round(elapsed * 1000, 2),
                }

                results.append(result)

                print(f"ERRO | {type(exc).__name__}: {exc}")

    finally:
        bus.shutdown()

    timestamp = datetime.now(UTC)

    filename = timestamp.strftime("ecu_data_%Y%m%d_%H%M%S.json")

    log_path = LOG_DIR / filename

    document = {
        "timestamp": timestamp.isoformat(),
        "tool": "19_uds_ecu_data_reader",
        "interface": "COM6",
        "bitrate": 500000,
        "tx_id": f"0x{TX_ID:08X}",
        "rx_id": f"0x{RX_ID:08X}",
        "flow_control_id": f"0x{FLOW_CONTROL_ID:08X}",
        "ecu": {
            "family": "IAW 10GF",
            "hardware": "MM10GFHW015",
            "supplier": "Magneti Marelli",
        },
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

    positive = sum(
        1
        for result in results
        if result["status"]
        in {
            "positive",
            "value_under_investigation",
        }
    )

    negative = sum(1 for result in results if result["status"] == "negative")

    errors = sum(1 for result in results if result["status"] == "error")

    print()
    print("================================")
    print("ECU Data Reader finalizado")
    print(f"DIDs positivos : {positive}")
    print(f"DIDs negativos : {negative}")
    print(f"Erros          : {errors}")
    print(f"Total          : {len(results)}")
    print(f"JSON           : {log_path}")
    print("================================")


if __name__ == "__main__":
    main()
