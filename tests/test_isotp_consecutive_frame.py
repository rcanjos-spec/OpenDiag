from opendiag.protocols.isotp import (
    FrameType,
    ISOTPFrame,
)


def test_parse_consecutive_frame() -> None:
    frame = ISOTPFrame.from_can_data(b"\x21\xaa\xbb\xcc\xdd\xee\xff\x11")

    assert frame.frame_type is FrameType.CONSECUTIVE

    assert frame.payload == (b"\xaa\xbb\xcc\xdd\xee\xff\x11")
