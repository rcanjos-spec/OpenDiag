from opendiag.bus.python_can import PythonCANBus
from opendiag.protocols.isotp_transport import ISOTPTransport
from opendiag.uds.client import UDSClient
from opendiag.uds.response_parser import UDSResponseParser
from opendiag.uds.response_registry import ResponseRegistry

bus = PythonCANBus(
    interface="slcan",
    channel="COM6",
    bitrate=500000,
)

try:
    transport = ISOTPTransport(
        bus=bus,
        tx_id=0x18DA10F1,
        tx_extended=True,
        rx_id=0x18DAF110,
        flow_control_id=0x18DA10F1,
        reassembly_timeout=5.0,
    )

    parser = UDSResponseParser(
        registry=ResponseRegistry(),
    )

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    print("## KACTOENG - UDS VIN Reader")
    print()
    print("Interface : COM6")
    print("Bitrate   : 500000")
    print("TX ID     : 18DA10F1")
    print("RX ID     : 18DAF110")
    print("FC ID     : 18DA10F1")
    print()
    print("Solicitando VIN...")
    print()

    vin = client.read_vin()

    print(f"VIN: {vin}")

finally:
    bus.shutdown()
