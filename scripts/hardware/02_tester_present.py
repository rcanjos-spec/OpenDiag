from opendiag.bus.python_can import PythonCANBus
from opendiag.protocols.isotp_transport import ISOTPTransport

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

    print("✅ Transporte criado!")

finally:
    if bus is not None:
        bus.shutdown()
