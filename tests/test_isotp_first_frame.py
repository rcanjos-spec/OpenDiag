from opendiag.protocols.isotp import (
    ISOTPFrame,
    ISOTPReassembler,
)


def test_reassembler_waits_for_consecutive_frame() -> None:
    reassembler = ISOTPReassembler()

    frame = ISOTPFrame.from_can_data(b"\x10\x09\x62\xf1\x90\x31\x47\x31")

    message = reassembler.feed(frame)

    assert message is None
