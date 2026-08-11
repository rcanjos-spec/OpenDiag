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


def test_receive_reassembles_multi_frame_message() -> None:
    bus = Mock()

    bus.receive.side_effect = [
        CANFrame(
            arbitration_id=0x7E8,
            data=bytes.fromhex("10 14 49 02 01 39 42 44"),
            timestamp=0.0,
        ),
        CANFrame(
            arbitration_id=0x7E8,
            data=bytes.fromhex("21 33 35 38 41 43 47 53"),
            timestamp=0.1,
        ),
        CANFrame(
            arbitration_id=0x7E8,
            data=bytes.fromhex("22 59 4E 34 34 35 30 30"),
            timestamp=0.2,
        ),
    ]

    transport = ISOTPTransport(
        bus=bus,
    )

    payload = transport.receive()

    assert payload == bytes.fromhex(
        "49 02 01 39 42 44 33 35 38 41 43 47 53 59 4E 34 34 35 30 30"
    )

    assert bus.receive.call_count == 3
