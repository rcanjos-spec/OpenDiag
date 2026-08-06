import time

import pytest

from opendiag.protocols.isotp import (
    ISOTPFrame,
    ISOTPReassembler,
)


def test_reassemble_single_frame() -> None:
    reassembler = ISOTPReassembler()

    frame = ISOTPFrame.from_can_data(b"\x03\x22\xf1\x90")

    message = reassembler.feed(frame)

    assert message is not None
    assert message.payload == b"\x22\xf1\x90"


def test_invalid_sequence_number() -> None:
    reassembler = ISOTPReassembler()

    first = ISOTPFrame.from_can_data(b"\x10\x09\x62\xf1\x90\x31\x47\x31")

    wrong = ISOTPFrame.from_can_data(b"\x25\x58\x58\x58")

    assert reassembler.feed(first) is None

    with pytest.raises(ValueError):
        reassembler.feed(wrong)


def test_reassembler_timeout() -> None:
    reassembler = ISOTPReassembler(timeout=0.1)

    first = ISOTPFrame.from_can_data(b"\x10\x09\x62\xf1\x90\x31\x47\x31")

    assert reassembler.feed(first) is None

    time.sleep(0.2)

    with pytest.raises(TimeoutError):
        reassembler.feed(ISOTPFrame.from_can_data(b"\x21\x58\x58\x58"))
