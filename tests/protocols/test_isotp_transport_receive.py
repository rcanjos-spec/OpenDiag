from unittest.mock import Mock

from opendiag.core.can_frame import CANFrame
from opendiag.protocols.isotp import ISOTPMessage
from opendiag.protocols.isotp_transport import ISOTPTransport


def test_receive_uses_bus() -> None:
    bus = Mock()

    bus.receive.return_value = CANFrame(
        arbitration_id=0x7E8,
        data=b"\x02\x7e\x00",
        timestamp=0.0,
    )

    reassembler = Mock()
    reassembler.feed.return_value = ISOTPMessage(
        payload=b"\x7e\x00",
    )

    transport = ISOTPTransport(
        bus=bus,
        reassembler=reassembler,
    )

    payload = transport.receive()

    assert payload == b"\x7e\x00"

    bus.receive.assert_called_once()
    reassembler.feed.assert_called_once()
