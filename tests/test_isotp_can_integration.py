from unittest.mock import Mock

from opendiag.core.can_frame import CANFrame
from opendiag.protocols.isotp import ISOTPFrame
from opendiag.protocols.isotp_transport import ISOTPTransport


def test_transport_sends_can_frame() -> None:
    bus = Mock()

    segmenter = Mock()
    segmenter.segment.return_value = [
        ISOTPFrame(
            payload=b"\x3e\x00",
        ),
    ]

    transport = ISOTPTransport(
        bus=bus,
        segmenter=segmenter,
    )

    transport.send(
        b"\x3e\x00",
    )

    frame = bus.send.call_args.args[0]

    assert isinstance(frame, CANFrame)


def test_transport_receives_can_frame() -> None:
    bus = Mock()

    bus.receive.return_value = CANFrame(
        arbitration_id=0x7E8,
        data=b"\x02\x7e\x00",
        timestamp=0.0,
    )

    transport = ISOTPTransport(
        bus=bus,
    )

    payload = transport.receive()

    assert payload == b"\x7e\x00"
