from opendiag.protocols.isotp import (
    FrameType,
    ISOTPFrame,
)


def test_parse_consecutive_frame() -> None:
    # Arrange
    data = b"\x21\xaa\xbb\xcc\xdd\xee\xff\x11"

    # Act
    frame = ISOTPFrame.from_can_data(data)

    # Assert
    assert frame.frame_type is FrameType.CONSECUTIVE
    assert frame.sequence_number == 1
    assert frame.payload == b"\xaa\xbb\xcc\xdd\xee\xff\x11"


def test_parse_consecutive_frame_sequence_number_15() -> None:
    # Arrange
    data = b"\x2f\xaa\xbb"

    # Act
    frame = ISOTPFrame.from_can_data(data)

    # Assert
    assert frame.frame_type is FrameType.CONSECUTIVE
    assert frame.sequence_number == 15
    assert frame.payload == b"\xaa\xbb"
