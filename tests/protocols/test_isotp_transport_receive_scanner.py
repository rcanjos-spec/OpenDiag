from unittest.mock import Mock

from opendiag.core.can_frame import CANFrame
from opendiag.protocols.isotp import (
    ISOTPMessage,
)
from opendiag.protocols.isotp_transport import ISOTPTransport


def test_receive_uses_scanner() -> None:
    scanner = Mock()

    scanner.receive.return_value = CANFrame(
        arbitration_id=0x7E8,
        data=b"\x02\x7e\x00",
        timestamp=0.0,
    )

    reassembler = Mock()
    reassembler.feed.return_value = ISOTPMessage(
        payload=b"\x7e\x00",
    )

    transport = ISOTPTransport(
        scanner=scanner,
        reassembler=reassembler,
    )

    payload = transport.receive()

    assert payload == b"\x7e\x00"

    scanner.receive.assert_called_once()
