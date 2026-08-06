from unittest.mock import MagicMock, patch

from opendiag.bus.python_can import PythonCANBus


@patch("opendiag.bus.python_can.can.Bus")
def test_create_python_can_bus(mock_bus: MagicMock) -> None:
    PythonCANBus(
        interface="virtual",
        channel="vcan0",
        bitrate=500000,
    )

    mock_bus.assert_called_once()
