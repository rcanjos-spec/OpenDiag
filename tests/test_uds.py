from unittest.mock import Mock

from opendiag.protocols.uds import UDSClient


def test_uds_client_sends_request_and_returns_response() -> None:
    transport = Mock()

    transport.receive.return_value = bytes.fromhex(
        "49 02 01 39 42 44 33 35 38 41 43 47 53 59 4E 34 34 35 30 30"
    )

    client = UDSClient(transport=transport)

    response = client.request(
        bytes.fromhex("09 02"),
    )

    assert response == bytes.fromhex(
        "49 02 01 39 42 44 33 35 38 41 43 47 53 59 4E 34 34 35 30 30"
    )

    transport.send.assert_called_once_with(
        bytes.fromhex("09 02"),
    )

    transport.receive.assert_called_once_with()
