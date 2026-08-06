from unittest.mock import Mock

from opendiag.protocols.isotp_transport import ISOTPTransport
from opendiag.uds.client import UDSClient
from opendiag.uds.services.tester_present import TesterPresent


def test_client_receives_response_through_isotp_transport() -> None:
    bus = Mock()

    segmenter = Mock()
    segmenter.segment.return_value = []

    payload = b"\x7e\x00"

    reassembler = Mock()
    reassembler.feed.return_value = payload

    transport = ISOTPTransport(
        bus=bus,
        segmenter=segmenter,
        reassembler=reassembler,
    )

    bus.receive.return_value = object()

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
