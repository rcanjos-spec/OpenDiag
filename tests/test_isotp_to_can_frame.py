from opendiag.core.can_frame import CANFrame
from opendiag.protocols.isotp import ISOTPFrame


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
