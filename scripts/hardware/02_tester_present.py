from opendiag.bus.python_can import PythonCANBus
from opendiag.protocols.isotp_transport import ISOTPTransport
from opendiag.uds.client import UDSClient
from opendiag.uds.response_parser import UDSResponseParser
from opendiag.uds.response_registry import ResponseRegistry


def main() -> None:
    bus = None

    try:
        bus = PythonCANBus(
            interface="slcan",
            channel="COM6",
            bitrate=500000,
        )

        transport = ISOTPTransport(
            bus=bus,
            tx_id=0x7E0,
        )

        parser = UDSResponseParser(
            registry=ResponseRegistry(),
        )

        client = UDSClient(
            transport=transport,
            parser=parser,
        )

        response = client.tester_present()

        print(f"Resposta ECU: {response}")

    finally:
        if bus is not None:
            bus.shutdown()


if __name__ == "__main__":
    main()
