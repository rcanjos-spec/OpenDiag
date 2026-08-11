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


def test_uds_client_reads_data_by_identifier() -> None:
    transport = Mock()

    transport.receive.return_value = bytes.fromhex(
        "62 F1 90 39 42 44 33 35 38 41 43 47 53 59 4E 34 34 35 30 30"
    )

    client = UDSClient(transport=transport)

    response = client.read_data_by_identifier(0xF190)

    assert response == bytes.fromhex(
        "62 F1 90 39 42 44 33 35 38 41 43 47 53 59 4E 34 34 35 30 30"
    )

    transport.send.assert_called_once_with(
        bytes.fromhex("22 F1 90"),
    )

    transport.receive.assert_called_once_with()


def test_uds_client_reads_vin() -> None:
    transport = Mock()

    transport.receive.return_value = bytes.fromhex(
        "62 F1 90 39 42 44 33 35 38 41 43 47 53 59 4E 34 34 35 30 30"
    )

    client = UDSClient(transport=transport)

    assert client.read_vin() == "9BD358ACGSYN44500"

    transport.send.assert_called_once_with(
        bytes.fromhex("22 F1 90"),
    )


def test_uds_client_starts_default_session() -> None:
    transport = Mock()

    transport.receive.return_value = bytes.fromhex("50 01 00 32 01 F4")

    client = UDSClient(transport=transport)

    response = client.start_diagnostic_session(0x01)

    assert response == bytes.fromhex("50 01 00 32 01 F4")

    transport.send.assert_called_once_with(
        bytes.fromhex("10 01"),
    )
