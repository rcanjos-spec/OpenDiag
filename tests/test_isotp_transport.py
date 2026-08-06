from unittest.mock import Mock, call

from opendiag.protocols.isotp import (
    ISOTPFrame,
    ISOTPMessage,
    ISOTPReassembler,
    ISOTPSegmenter,
)
from opendiag.protocols.isotp_transport import ISOTPTransport
from opendiag.transport.mock import MockTransport


def test_create_isotp_transport() -> None:
    transport = ISOTPTransport(
        bus=object(),
    )

    assert transport is not None


def test_transport_sends_data_to_bus() -> None:
    bus = Mock()

    transport = ISOTPTransport(
        bus=bus,
    )

    transport.send(
        b"\x3e\x00",
    )

    frame = bus.send.call_args.args[0]
    assert frame.payload == b"\x3e\x00"
    assert frame.length == 2


def test_transport_receives_data_from_bus() -> None:
    bus = Mock()

    bus.receive.return_value = ISOTPFrame.from_can_data(
        b"\x02\x7e\x00",
    )
    transport = ISOTPTransport(
        bus=bus,
    )

    data = transport.receive()

    assert isinstance(data, ISOTPMessage)
    assert data.payload == b"\x7e\x00"


def test_transport_uses_segmenter_to_send() -> None:
    bus = Mock()

    frame = object()

    segmenter = Mock()
    segmenter.segment.return_value = [frame]

    transport = ISOTPTransport(
        bus=bus,
        segmenter=segmenter,
    )

    transport.send(
        b"\x22\xf1\x90",
    )

    segmenter.segment.assert_called_once_with(
        b"\x22\xf1\x90",
    )

    bus.send.assert_called_once_with(frame)


def test_transport_uses_reassembler_to_receive() -> None:
    bus = Mock()

    frame = object()

    bus.receive.return_value = frame

    message = object()

    reassembler = Mock()
    reassembler.feed.return_value = message

    transport = ISOTPTransport(
        bus=bus,
        segmenter=Mock(),
        reassembler=reassembler,
    )

    result = transport.receive()

    reassembler.feed.assert_called_once_with(frame)

    assert result is message


def test_transport_sends_all_segmented_frames() -> None:
    bus = Mock()

    frames = [
        object(),
        object(),
        object(),
    ]

    segmenter = Mock()
    segmenter.segment.return_value = frames

    transport = ISOTPTransport(
        bus=bus,
        segmenter=segmenter,
        reassembler=Mock(),
    )

    transport.send(
        b"0123456789ABCDEF",
    )

    bus.send.assert_has_calls(
        [
            call(frames[0]),
            call(frames[1]),
            call(frames[2]),
        ]
    )

    assert bus.send.call_count == 3


def test_transport_uses_real_isotp_components() -> None:
    transport = ISOTPTransport(
        bus=MockTransport(),
        segmenter=ISOTPSegmenter(),
        reassembler=ISOTPReassembler(),
    )

    assert transport is not None
