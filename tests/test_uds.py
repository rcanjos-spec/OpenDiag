from unittest.mock import Mock

import pytest

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


def test_uds_client_detects_negative_response() -> None:
    transport = Mock()

    transport.receive.return_value = bytes.fromhex("7F 10 12")

    client = UDSClient(transport=transport)

    response = client.request(bytes.fromhex("10 02"))

    assert response == bytes.fromhex("7F 10 12")

    transport.send.assert_called_once_with(
        bytes.fromhex("10 02"),
    )


def test_uds_client_parses_negative_response() -> None:
    response = bytes.fromhex("7F 10 12")

    negative = UDSClient.parse_negative_response(response)

    assert negative.service_id == 0x10
    assert negative.nrc == 0x12


def test_uds_client_rejects_invalid_negative_response() -> None:
    with pytest.raises(ValueError, match="Invalid UDS negative response"):
        UDSClient.parse_negative_response(bytes.fromhex("50 01 00"))


def test_uds_negative_response_has_nrc_description() -> None:
    response = UDSClient.parse_negative_response(bytes.fromhex("7F 10 12"))

    assert response.nrc_description == "SubFunctionNotSupported"
