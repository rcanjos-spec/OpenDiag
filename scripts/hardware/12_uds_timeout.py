import time

from opendiag.bus.python_can import PythonCANBus
from opendiag.protocols.isotp_transport import ISOTPTransport

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

    print("## OpenDiag - ISO-TP Physical Timeout Test")
    print()
    print("Interface : COM6")
    print("Bitrate   : 500000")
    print("RX ID     : 18DAF110")
    print()
    print("Aguardando frames por 2 segundos...")
    print()

    start = time.monotonic()

    try:
        transport.receive(timeout=2.0)
    except TimeoutError as exc:
        elapsed = time.monotonic() - start

        print("Timeout:", exc)
        print(f"Tempo decorrido: {elapsed:.3f} s")

finally:
    bus.shutdown()
