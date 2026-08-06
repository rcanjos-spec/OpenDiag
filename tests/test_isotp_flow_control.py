from opendiag.protocols.isotp import (
    FrameType,
    ISOTPFrame,
)


def test_parse_flow_control_frame() -> None:
    frame = ISOTPFrame.from_can_data(b"\x30\x00\x00")

    assert frame.frame_type is FrameType.FLOW_CONTROL

    assert frame.payload == b""
