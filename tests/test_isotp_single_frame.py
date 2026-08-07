import pytest

from opendiag.protocols.isotp import (
    FrameType,
    ISOTPFrame,
)


def test_parse_single_frame() -> None:
    frame = ISOTPFrame.from_can_data(
        b"\x03\x22\xf1\x90",
    )

    assert frame.frame_type is FrameType.SINGLE
    assert frame.length == 3
    assert frame.payload == b"\x22\xf1\x90"


def test_single_frame_length_matches_payload() -> None:
    frame = ISOTPFrame.from_can_data(
        b"\x02\x10\x03",
    )

    assert frame.length == len(frame.payload)


def test_single_frame_ignores_padding() -> None:
    frame = ISOTPFrame.from_can_data(
        b"\x03\x22\xf1\x90\xaa\xaa\xaa\xaa",
    )

    assert frame.frame_type is FrameType.SINGLE
    assert frame.length == 3
    assert frame.payload == b"\x22\xf1\x90"


def test_parse_empty_single_frame() -> None:
    frame = ISOTPFrame.from_can_data(b"\x00")

    assert frame.frame_type is FrameType.SINGLE
    assert frame.length == 0
    assert frame.payload == b""


def test_parse_empty_can_data_raises_index_error() -> None:
    with pytest.raises(IndexError):
        ISOTPFrame.from_can_data(b"")
