from unittest.mock import Mock

from opendiag.protocols.isotp import ISOTPFrame
from opendiag.protocols.isotp_transport import ISOTPTransport


def test_transport_sends_frame_through_scanner() -> None:
    scanner = Mock()

    segmenter = Mock()
    segmenter.segment.return_value = [
        ISOTPFrame(
            payload=b"\x3e\x00",
        )
    ]

    transport = ISOTPTransport(
        scanner=scanner,
        segmenter=segmenter,
    )

    transport.send(b"\x3e\x00")

    scanner.send.assert_called_once()
