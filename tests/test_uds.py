from unittest.mock import Mock

import pytest

from opendiag.protocols.uds import (
    UDSClient,
    UDSNegativeResponseError,
)


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

    transport.receive.assert_called_once()
    assert "timeout" in transport.receive.call_args.kwargs


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


def test_uds_client_request_positive_rejects_negative_response() -> None:
    transport = Mock()

    transport.receive.return_value = bytes.fromhex("7F 10 12")

    client = UDSClient(transport=transport)

    with pytest.raises(ValueError, match="Negative UDS response"):
        client.request_positive(
            bytes.fromhex("10 01"),
        )


def test_uds_client_rejects_negative_diagnostic_session() -> None:
    transport = Mock()

    transport.receive.return_value = bytes.fromhex("7F 10 12")

    client = UDSClient(transport=transport)

    with pytest.raises(ValueError, match="Negative UDS response"):
        client.start_diagnostic_session(0x02)


def test_uds_client_rejects_negative_read_data_by_identifier() -> None:
    transport = Mock()

    transport.receive.return_value = bytes.fromhex("7F 22 31")

    client = UDSClient(transport=transport)

    with pytest.raises(ValueError, match="Negative UDS response"):
        client.read_data_by_identifier(0xF190)


def test_uds_negative_response_raises_uds_error() -> None:
    transport = Mock()

    transport.receive.return_value = bytes.fromhex("7F 22 31")

    client = UDSClient(transport=transport)

    with pytest.raises(UDSNegativeResponseError) as exc_info:
        client.request_positive(bytes.fromhex("22 F1 90"))

    error = exc_info.value

    assert error.service_id == 0x22
    assert error.nrc == 0x31
    assert error.nrc_description == "RequestOutOfRange"


def test_uds_client_request_positive_ignores_response_pending() -> None:
    transport = Mock()

    transport.receive.side_effect = [
        bytes.fromhex("7F 10 78"),
        bytes.fromhex("50 01 00 32 01 F4"),
    ]

    client = UDSClient(transport=transport)

    response = client.request_positive(
        bytes.fromhex("10 01"),
    )

    assert response == bytes.fromhex("50 01 00 32 01 F4")

    assert transport.receive.call_count == 2


def test_uds_client_request_positive_times_out_on_response_pending() -> None:
    transport = Mock()

    transport.receive.return_value = bytes.fromhex("7F 10 78")

    client = UDSClient(transport=transport)

    with pytest.raises(TimeoutError, match="UDS response pending timeout"):
        client.request_positive(
            bytes.fromhex("10 01"),
            timeout=0.01,
        )


def test_uds_client_request_positive_response() -> None:
    transport = Mock()

    transport.receive.return_value = bytes.fromhex("50 01 00 32 01 F4")

    client = UDSClient(transport=transport)

    response = client.request_positive(
        bytes.fromhex("10 01"),
    )

    assert response == bytes.fromhex("50 01 00 32 01 F4")

    transport.send.assert_called_once_with(
        bytes.fromhex("10 01"),
    )

    transport.receive.assert_called_once()

    timeout = transport.receive.call_args.kwargs["timeout"]

    assert timeout > 0
    assert timeout <= 1.0


def test_uds_client_reads_dtc_information() -> None:
    transport = Mock()

    transport.receive.return_value = bytes.fromhex("59 02 CF 01 07 00 0F 01 30 00 40")

    client = UDSClient(transport=transport)

    dtcs = client.read_dtc_information(
        0x02,
        status_mask=0xFF,
    )

    assert len(dtcs) == 2

    assert dtcs[0].code == 0x010700
    assert dtcs[0].status == 0x0F

    assert dtcs[1].code == 0x013000
    assert dtcs[1].status == 0x40

    transport.send.assert_called_once_with(
        bytes.fromhex("19 02 FF"),
    )


def test_uds_client_rejects_negative_dtc_information() -> None:
    transport = Mock()

    transport.receive.return_value = bytes.fromhex("7F 19 12")

    client = UDSClient(transport=transport)

    with pytest.raises(UDSNegativeResponseError) as exc_info:
        client.read_dtc_information(0x02)

    error = exc_info.value

    assert error.service_id == 0x19
    assert error.nrc == 0x12
    assert error.nrc_description == "SubFunctionNotSupported"


def test_uds_client_parses_dtc_information() -> None:
    response = bytes.fromhex("59 02 CF 01 23 45 67")

    dtcs = UDSClient.parse_dtc_information(response)

    assert len(dtcs) == 1
    assert dtcs[0].code == 0x012345
    assert dtcs[0].status == 0x67


def test_uds_client_rejects_invalid_dtc_information() -> None:
    response = bytes.fromhex("59 02 CF 01 23")

    with pytest.raises(ValueError, match="Invalid UDS DTC response"):
        UDSClient.parse_dtc_information(response)


def test_uds_client_parses_multiple_dtcs() -> None:
    response = bytes.fromhex("59 02 CF 01 23 45 67 06 78 9A 80")

    dtcs = UDSClient.parse_dtc_information(response)

    assert len(dtcs) == 2

    assert dtcs[0].code == 0x012345
    assert dtcs[0].status == 0x67

    assert dtcs[1].code == 0x06789A
    assert dtcs[1].status == 0x80


def test_uds_client_parses_no_dtcs() -> None:
    response = bytes.fromhex("59 02")

    dtcs = UDSClient.parse_dtc_information(response)

    assert dtcs == []
