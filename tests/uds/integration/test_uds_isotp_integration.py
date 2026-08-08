from unittest.mock import Mock

from opendiag.core.can_frame import CANFrame
from opendiag.protocols.isotp import ISOTPMessage
from opendiag.protocols.isotp_transport import ISOTPTransport
from opendiag.uds.client import UDSClient
from opendiag.uds.services.tester_present import TesterPresent


def test_client_receives_response_through_isotp_transport() -> None:
    bus = Mock()

    segmenter = Mock()
    segmenter.segment.return_value = []

    payload = b"\x7e\x00"
    reassembler = Mock()
    reassembler.feed.return_value = ISOTPMessage(
        payload=b"\x7e\x00",
    )

    transport = ISOTPTransport(
        bus=bus,
        segmenter=segmenter,
        reassembler=reassembler,
    )

    bus.receive.return_value = CANFrame(
        arbitration_id=0x7E8,
        data=b"\x02\x7e\x00",
        timestamp=0.0,
    )

    parser = Mock()
    parser.parse.return_value = "OK"

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    request = TesterPresent(
        suppress_response=False,
    )

    response = client.send(request)

    parser.parse.assert_called_once_with(
        payload,
    )

    assert response == "OK"
