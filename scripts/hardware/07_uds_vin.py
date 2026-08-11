from opendiag.bus.python_can import PythonCANBus
from opendiag.obd import OBDClient
from opendiag.protocols.isotp_transport import ISOTPTransport


def main() -> None:
    bus = PythonCANBus(
        interface="slcan",
        channel="COM6",
        bitrate=500000,
    )

    try:
        transport = ISOTPTransport(
            bus=bus,
            tx_id=0x18DB33F1,
            tx_extended=True,
            rx_id=0x18DAF110,
            flow_control_id=0x18DA10F1,
        )

        client = OBDClient(
            transport=transport,
        )

        print("OpenDiag - UDS VIN Reader")
        print("-------------------------")
        print("Interface : COM6")
        print("Bitrate   : 500000")
        print("TX ID     : 18DB33F1")
        print("RX ID     : 18DAF110")
        print("FC ID     : 18DA10F1")
        print()
        print("Solicitando VIN...")

        vin = client.read_vin()

        print()
        print(f"VIN: {vin}")

    finally:
        bus.shutdown()


if __name__ == "__main__":
    main()
