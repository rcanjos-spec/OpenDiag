import pytest

from opendiag.bus.mock import MockCANBus
from opendiag.core.can_frame import CANFrame
from opendiag.core.exceptions import BusError


def test_send_and_receive_frame() -> None:
    bus = MockCANBus()

    frame = CANFrame(
        arbitration_id=0x7E0,
        data=b"\x02\x10\x03",
        timestamp=0.0,
    )

    bus.send(frame)

    received = bus.receive()

    assert received == frame


def test_receive_empty_bus() -> None:
    bus = MockCANBus()

    with pytest.raises(BusError):
        bus.receive()
