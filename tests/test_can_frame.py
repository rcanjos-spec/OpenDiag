from opendiag.core.can_frame import CANFrame


def test_can_frame_creation() -> None:
    frame = CANFrame(
        arbitration_id=0x7E0,
        data=b"\x02\x10\x03",
        timestamp=0.0,
    )

    assert frame.arbitration_id == 0x7E0
    assert frame.data == b"\x02\x10\x03"
    assert frame.timestamp == 0.0
    assert frame.is_extended_id is False
    assert frame.is_remote_frame is False


def test_can_frame_dlc() -> None:
    frame = CANFrame(
        arbitration_id=0x7E0,
        data=b"\x02\x10\x03",
        timestamp=0.0,
    )

    assert frame.dlc == 3
