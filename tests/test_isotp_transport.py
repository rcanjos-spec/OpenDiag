from unittest.mock import Mock, call

from opendiag.core.can_frame import CANFrame
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

    assert isinstance(frame, CANFrame)
    assert frame.data == b"\x02\x3e\x00"
    assert frame.arbitration_id == 0x7E0


def test_transport_receives_data_from_bus() -> None:
    bus = Mock()

    bus.receive.return_value = CANFrame(
        arbitration_id=0x7E8,
        data=b"\x02\x7e\x00",
        timestamp=0.0,
    )

    transport = ISOTPTransport(
        bus=bus,
    )

    data = transport.receive()

    assert data == b"\x7e\x00"


def test_transport_uses_segmenter_to_send() -> None:
    bus = Mock()

    frame = Mock()

    can_frame = Mock()
    frame.to_can_frame.return_value = can_frame

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

    frame.to_can_frame.assert_called_once_with(
        arbitration_id=0x7E0,
    )

    bus.send.assert_called_once_with(can_frame)


def test_transport_uses_reassembler_to_receive() -> None:
    bus = Mock()

    can_frame = CANFrame(
        arbitration_id=0x7E8,
        data=b"\x02\x7e\x00",
        timestamp=0.0,
    )

    bus.receive.return_value = can_frame

    reassembler = Mock()

    reassembler.feed.return_value = ISOTPMessage(
        payload=b"\x7e\x00",
    )

    transport = ISOTPTransport(
        bus=bus,
        segmenter=Mock(),
        reassembler=reassembler,
    )

    result = transport.receive()

    reassembler.feed.assert_called_once()

    frame = reassembler.feed.call_args.args[0]

    assert isinstance(frame, ISOTPFrame)
    assert result == b"\x7e\x00"


def test_transport_sends_all_segmented_frames() -> None:
    bus = Mock()

    frames = []

    for _ in range(3):
        frame = Mock()
        frame.to_can_frame.return_value = Mock()
        frames.append(frame)

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
            call(frames[0].to_can_frame.return_value),
            call(frames[1].to_can_frame.return_value),
            call(frames[2].to_can_frame.return_value),
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
