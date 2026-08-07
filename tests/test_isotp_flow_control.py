from opendiag.protocols.isotp import (
    FrameType,
    ISOTPFrame,
)


def test_parse_flow_control_frame() -> None:
    # Arrange
    data = b"\x30\x00\x00"

    # Act
    frame = ISOTPFrame.from_can_data(data)

    # Assert
    assert frame.frame_type is FrameType.FLOW_CONTROL
    assert frame.payload == b""


def test_parse_flow_control_wait_frame() -> None:
    # Arrange
    data = b"\x31\x00\x00"

    # Act
    frame = ISOTPFrame.from_can_data(data)

    # Assert
    assert frame.frame_type is FrameType.FLOW_CONTROL
