from opendiag.bus.python_can import PythonCANBus
from opendiag.protocols.isotp_transport import ISOTPTransport
from opendiag.protocols.uds import UDSClient

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
    )

    client = UDSClient(transport=transport)

    print("## OpenDiag - UDS Diagnostic Session")
    print()
    print("Interface : COM6")
    print("Bitrate   : 500000")
    print("TX ID     : 18DA10F1")
    print("RX ID     : 18DAF110")
    print("FC ID     : 18DA10F1")
    print()
    print("Solicitando Default Session...")
    print()

    response = client.start_diagnostic_session(0x01)

    print("Resposta:", response.hex(" ").upper())

finally:
    bus.shutdown()
