from unittest.mock import MagicMock

import can

from opendiag.bus.python_can import PythonCANBus
from opendiag.core.can_frame import CANFrame


def test_send_can_frame() -> None:
    mock_bus = MagicMock()

    bus = PythonCANBus(
        interface="virtual",
        channel="vcan0",
        bitrate=500000,
        bus=mock_bus,
    )

    frame = CANFrame(
        arbitration_id=0x7E0,
        data=b"\x02\x3e\x00",
        timestamp=0.0,
    )

    bus.send(frame)

    mock_bus.send.assert_called_once()

    message = mock_bus.send.call_args.args[0]

    assert isinstance(message, can.Message)
    assert message.arbitration_id == 0x7E0
    assert message.data == b"\x02\x3e\x00"
    assert message.is_extended_id is False


def test_receive_can_frame() -> None:
    mock_bus = MagicMock()

    mock_bus.recv.return_value = can.Message(
        arbitration_id=0x7E8,
        data=b"\x02\x7e\x00",
        is_extended_id=False,
    )

    bus = PythonCANBus(
        interface="virtual",
        channel="vcan0",
        bitrate=500000,
        bus=mock_bus,
    )

    frame = bus.receive()

    assert isinstance(frame, CANFrame)
    assert frame.arbitration_id == 0x7E8
    assert frame.data == b"\x02\x7e\x00"
    assert frame.is_extended_id is False

    mock_bus = MagicMock()

    mock_bus.recv.return_value = can.Message(
        arbitration_id=0x7E8,
        data=b"\x02\x7e\x00",
        is_extended_id=False,
    )

    bus = PythonCANBus(
        interface="virtual",
        channel="vcan0",
        bitrate=500000,
        bus=mock_bus,
    )

    frame = bus.receive()

    assert isinstance(frame, CANFrame)
    assert frame.arbitration_id == 0x7E8
    assert frame.data == b"\x02\x7e\x00"
    assert frame.is_extended_id is False


def test_receive_timeout() -> None:
    mock_bus = MagicMock()
    mock_bus.recv.return_value = None

    bus = PythonCANBus(
        interface="virtual",
        channel="vcan0",
        bitrate=500000,
        bus=mock_bus,
    )

    frame = bus.receive(timeout=1.0)

    assert frame is None
    mock_bus.recv.assert_called_once_with(timeout=1.0)
