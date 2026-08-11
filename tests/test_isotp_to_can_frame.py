from opendiag.core.can_frame import CANFrame
from opendiag.protocols.isotp import FrameType, ISOTPFrame


def test_isotp_frame_to_can_frame() -> None:
    frame = ISOTPFrame(
        payload=b"\x3e\x00",
    )

    can_frame = frame.to_can_frame(
        arbitration_id=0x7E0,
    )

    assert isinstance(can_frame, CANFrame)
    assert can_frame.arbitration_id == 0x7E0
    assert can_frame.data == b"\x02\x3e\x00"


def test_first_frame_to_can_frame() -> None:
    frame = ISOTPFrame(
        payload=b"\x10\x03\x22\xf1\x90\x01",
        frame_type=FrameType.FIRST,
        message_length=20,
    )

    can_frame = frame.to_can_frame(
        arbitration_id=0x7E0,
    )

    assert can_frame.arbitration_id == 0x7E0
    assert can_frame.data == (b"\x10\x14\x10\x03\x22\xf1\x90\x01")


def test_to_can_frame_preserves_extended_id() -> None:
    frame = ISOTPFrame(
        payload=b"\x09\x02",
    )

    can_frame = frame.to_can_frame(
        arbitration_id=0x18DB33F1,
        is_extended_id=True,
    )

    assert can_frame.arbitration_id == 0x18DB33F1
    assert can_frame.data == b"\x02\x09\x02"
    assert can_frame.is_extended_id is True
