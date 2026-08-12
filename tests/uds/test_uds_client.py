from unittest.mock import Mock

import pytest

from opendiag.uds.client import UDSClient
from opendiag.uds.reset import ResetType
from opendiag.uds.response_parser import UDSResponseParser
from opendiag.uds.response_registry import ResponseRegistry
from opendiag.uds.responses.read_dtc_information import (
    ReadDTCInformationResponse,
)
from opendiag.uds.security import SecurityLevel
from opendiag.uds.services.tester_present import TesterPresent
from opendiag.uds.session import SessionType


def test_create_client() -> None:
    client = UDSClient(
        transport=object(),
        parser=object(),
    )

    assert client is not None


def test_send_request() -> None:
    transport = Mock()
    parser = Mock()

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    request = TesterPresent()

    client.send(request)

    transport.send.assert_called_once_with(request.data)


def test_send_receives_response() -> None:
    transport = Mock()
    transport.receive.return_value = b"\x7e\x00"

    parser = Mock()

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    client.send(TesterPresent())

    transport.receive.assert_called_once_with()


def test_send_uses_parser() -> None:
    transport = Mock()
    transport.receive.return_value = b"\x7e\x00"

    parser = Mock()

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    client.send(
        TesterPresent(),
    )

    parser.parse.assert_called_once_with(
        b"\x7e\x00",
    )


def test_send_returns_response() -> None:
    transport = Mock()
    transport.receive.return_value = b"\x7e\x00"

    expected = object()

    parser = Mock()
    parser.parse.return_value = expected

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    response = client.send(TesterPresent())

    assert response is expected


def test_ecu_reset() -> None:
    transport = Mock()

    transport.receive.return_value = b"\x51\x03"

    parser = Mock()

    parser.parse.return_value = "OK"

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    response = client.ecu_reset(
        ResetType.SOFT,
    )

    transport.send.assert_called_once_with(
        b"\x11\x03",
    )

    parser.parse.assert_called_once_with(
        b"\x51\x03",
    )

    assert response == "OK"


def test_security_access() -> None:
    transport = Mock()

    transport.receive.return_value = b"\x67\x01\x12\x34\x56\x78"

    parser = Mock()
    parser.parse.return_value = "OK"

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    response = client.security_access(
        level=SecurityLevel.LEVEL_1_REQUEST_SEED,
    )

    transport.send.assert_called_once_with(
        b"\x27\x01",
    )

    parser.parse.assert_called_once_with(
        b"\x67\x01\x12\x34\x56\x78",
    )

    assert response == "OK"


def test_uds_client_reads_dtc_information() -> None:
    transport = Mock()

    transport.receive.return_value = bytes.fromhex("59 02 CF 01 07 00 0F 01 30 00 40")

    client = UDSClient(
        transport=transport,
        parser=UDSResponseParser(
            registry=ResponseRegistry(),
        ),
    )

    response = client.read_dtc_information()

    assert isinstance(
        response,
        ReadDTCInformationResponse,
    )

    assert response.sid == 0x59
    assert response.subfunction == 0x02
    assert response.status_availability_mask == 0xCF

    assert len(response.dtcs) == 2

    assert response.dtcs[0].code == 0x010700
    assert response.dtcs[0].status == 0x0F

    assert response.dtcs[1].code == 0x013000
    assert response.dtcs[1].status == 0x40

    transport.send.assert_called_once_with(
        bytes.fromhex("19 02 FF"),
    )


def test_tester_present() -> None:
    transport = Mock()
    transport.receive.return_value = b"\x7e\x00"

    parser = Mock()
    parser.parse.return_value = "OK"

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    response = client.tester_present()

    transport.send.assert_called_once_with(
        b"\x3e\x00",
    )

    transport.receive.assert_called_once_with()

    parser.parse.assert_called_once_with(
        b"\x7e\x00",
    )

    assert response == "OK"


def test_diagnostic_session_control() -> None:
    transport = Mock()
    transport.receive.return_value = b"\x50\x03"

    parser = Mock()
    parser.parse.return_value = "OK"

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    response = client.diagnostic_session_control(
        SessionType.EXTENDED,
    )

    transport.send.assert_called_once_with(
        b"\x10\x03",
    )

    parser.parse.assert_called_once_with(
        b"\x50\x03",
    )

    assert response == "OK"


def test_uds_client_reads_data_by_identifier() -> None:
    transport = Mock()

    transport.receive.return_value = bytes.fromhex(
        "62 F1 90 31 48 47 43 4D 38 32 36 33 33 41 30 30 34 33 35 32"
    )

    client = UDSClient(
        transport=transport,
        parser=UDSResponseParser(
            registry=ResponseRegistry(),
        ),
    )

    response = client.read_data_by_identifier(
        0xF190,
    )

    assert response.did == 0xF190
    assert response.value == b"1HGCM82633A004352"

    transport.send.assert_called_once_with(
        bytes.fromhex("22 F1 90"),
    )


def test_read_vin() -> None:
    transport = Mock()

    transport.receive.return_value = b"\x62\xf1\x90" + b"1HGCM82633A004352"

    client = UDSClient(
        transport=transport,
        parser=UDSResponseParser(
            registry=ResponseRegistry(),
        ),
    )

    vin = client.read_vin()

    assert vin == "1HGCM82633A004352"

    transport.send.assert_called_once_with(
        bytes.fromhex("22 F1 90"),
    )


def test_read_vin_rejects_invalid_length() -> None:
    transport = Mock()

    transport.receive.return_value = b"\x62\xf1\x90" + b"123"

    client = UDSClient(
        transport=transport,
        parser=UDSResponseParser(
            registry=ResponseRegistry(),
        ),
    )

    with pytest.raises(ValueError, match="VIN must contain 17 characters"):
        client.read_vin()


def test_read_vin_rejects_non_ascii() -> None:
    transport = Mock()

    transport.receive.return_value = b"\x62\xf1\x90" + b"1HGCM82633A00435\xff"

    client = UDSClient(
        transport=transport,
        parser=UDSResponseParser(
            registry=ResponseRegistry(),
        ),
    )

    with pytest.raises(
        ValueError,
        match="VIN must contain ASCII characters",
    ):
        client.read_vin()
