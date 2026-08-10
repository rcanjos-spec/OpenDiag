import time

from opendiag.bus.python_can import PythonCANBus
from opendiag.protocols.isotp_transport import ISOTPTransport


def test_isotp_transport_over_virtual_can() -> None:
    channel = f"opendiag-isotp-{time.monotonic_ns()}"

    tx_bus = PythonCANBus(
        interface="virtual",
        channel=channel,
        bitrate=500000,
    )

    rx_bus = PythonCANBus(
        interface="virtual",
        channel=channel,
        bitrate=500000,
    )

    tx_transport = ISOTPTransport(
        bus=tx_bus,
    )

    rx_transport = ISOTPTransport(
        bus=rx_bus,
    )

    try:
        payload = b"\x3e\x00"

        tx_transport.send(payload)

        received = rx_transport.receive()

        assert received == payload

    finally:
        tx_bus.shutdown()
        rx_bus.shutdown()
