from opendiag.protocols.isotp import (
    ISOTPFrameType,
    ISOTPSegmenter,
)


def test_segment_single_frame() -> None:
    segmenter = ISOTPSegmenter()

    frames = list(segmenter.segment(b"\x22\xf1\x90"))

    assert len(frames) == 1

    assert frames[0].frame_type is ISOTPFrameType.SINGLE

    assert frames[0].payload == (b"\x22\xf1\x90")
