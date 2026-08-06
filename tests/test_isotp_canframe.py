from unittest.mock import Mock

from opendiag.core.can_frame import CANFrame
from opendiag.protocols.isotp import ISOTPFrame
from opendiag.protocols.isotp_transport import ISOTPTransport


def test_transport_converts_isotp_frame_to_can_frame() -> None:
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
