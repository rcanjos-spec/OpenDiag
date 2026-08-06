from unittest.mock import MagicMock

from opendiag.protocols.isotp_transport import ISOTPTransport
from opendiag.uds.client import UDSClient


def test_client_sends_tester_present() -> None:
    transport = MagicMock(spec=ISOTPTransport)
    parser = MagicMock()

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    client.tester_present()

    transport.send.assert_called_once_with(
        b"\x3e\x00",
    )
