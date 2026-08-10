from unittest.mock import MagicMock

from opendiag.bus.python_can import PythonCANBus
from opendiag.protocols.isotp_transport import ISOTPTransport


def test_transport_sends_using_python_can_bus() -> None:
    mock_can = MagicMock()

    bus = PythonCANBus(
        interface="virtual",
        channel="vcan0",
        bitrate=500000,
        bus=mock_can,
    )

    transport = ISOTPTransport(
        bus=bus,
    )

    transport.send(
        b"\x3e\x00",
    )

    mock_can.send.assert_called_once()
