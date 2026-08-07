from opendiag.protocols.isotp import (
    FrameType,
    ISOTPSegmenter,
)


def test_segment_single_frame() -> None:
    # Arrange
    segmenter = ISOTPSegmenter()
    payload = b"\x22\xf1\x90"

    # Act
    frames = list(segmenter.segment(payload))

    # Assert
    assert len(frames) == 1
    assert frames[0].frame_type is FrameType.SINGLE
    assert frames[0].payload == payload


def test_segment_multi_frame_message() -> None:
    # Arrange
    segmenter = ISOTPSegmenter()

    payload = b"\x62\xf1\x90\x31\x47\x31\x58\x58\x58"

    # Act
    frames = list(segmenter.segment(payload))

    # Assert
    assert len(frames) == 2

    assert frames[0].frame_type is FrameType.FIRST
    assert frames[1].frame_type is FrameType.CONSECUTIVE
