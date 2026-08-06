from unittest.mock import MagicMock

from opendiag.protocols.isotp_transport import ISOTPTransport
from opendiag.uds.client import UDSClient


def test_client_receives_tester_present_response() -> None:
    transport = MagicMock(spec=ISOTPTransport)
    parser = MagicMock()

    transport.receive.return_value = b"\x7e\x00"

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    client.tester_present()

    parser.parse.assert_called_once_with(
        b"\x7e\x00",
    )
