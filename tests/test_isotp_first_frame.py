from opendiag.protocols.isotp import (
    ISOTPFrame,
    ISOTPMessage,
    ISOTPReassembler,
)


def test_reassembler_completes_message() -> None:
    reassembler = ISOTPReassembler()

    first = ISOTPFrame.from_can_data(
        b"\x10\x09\x62\xf1\x90\x31\x47\x31",
    )

    consecutive = ISOTPFrame.from_can_data(
        b"\x21\x58\x58\x58",
    )

    assert reassembler.feed(first) is None

    message = reassembler.feed(consecutive)

    assert isinstance(
        message,
        ISOTPMessage,
    )

    assert message.payload == b"\x62\xf1\x90\x31\x47\x31\x58\x58\x58"
