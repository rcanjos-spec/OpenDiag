from opendiag.core.can_frame import CANFrame
from opendiag.utils.frame_formatter import FrameFormatter


def test_format_standard_frame() -> None:
    frame = CANFrame(
        arbitration_id=0x7E0,
        data=b"\x02\x10\x03",
        timestamp=0.0,
    )

    formatter = FrameFormatter()

    assert formatter.format(frame) == "7E0 [3] 02 10 03"
