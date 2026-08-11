from opendiag.protocols.isotp import (
    FrameType,
    ISOTPFrame,
    ISOTPReassembler,
)


def test_single_frame_creation() -> None:
    frame = ISOTPFrame(payload=b"\x22\xf1\x90")

    assert frame.payload == b"\x22\xf1\x90"


def test_reassembler_accepts_sequence_number_rollover() -> None:
    reassembler = ISOTPReassembler()

    first = ISOTPFrame(
        payload=b"\x59\x02" + bytes(4),
        frame_type=FrameType.FIRST,
        message_length=118,
    )

    assert reassembler.feed(first) is None

    for sequence_number in range(1, 16):
        frame = ISOTPFrame(
            payload=bytes([sequence_number]) * 7,
            frame_type=FrameType.CONSECUTIVE,
            sequence_number=sequence_number,
        )

        assert reassembler.feed(frame) is None

    rollover_frame = ISOTPFrame(
        payload=b"\x00" * 7,
        frame_type=FrameType.CONSECUTIVE,
        sequence_number=0,
    )

    message = reassembler.feed(rollover_frame)

    assert message is not None
    assert len(message.payload) == 118
