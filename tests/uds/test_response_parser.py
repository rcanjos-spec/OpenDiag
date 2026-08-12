from opendiag.uds.reset import ResetType
from opendiag.uds.response import NegativeResponse
from opendiag.uds.response_parser import UDSResponseParser
from opendiag.uds.response_registry import ResponseRegistry
from opendiag.uds.responses.diagnostic_session_control import (
    DiagnosticSessionControlResponse,
)
from opendiag.uds.responses.ecu_reset import ECUResetResponse
from opendiag.uds.responses.read_data_by_identifier import (
    ReadDataByIdentifierResponse,
)
from opendiag.uds.responses.read_dtc_information import (
    ReadDTCInformationResponse,
)
from opendiag.uds.responses.security_access import (
    SecurityAccessResponse,
)
from opendiag.uds.security import SecurityLevel
from opendiag.uds.session import SessionType


def test_parse_read_data_by_identifier() -> None:
    registry = ResponseRegistry()

    registry.register(
        0x62,
        ReadDataByIdentifierResponse,
    )

    parser = UDSResponseParser(
        registry=registry,
    )

    response = parser.parse(
        b"\x62\xf1\x90ABC",
    )

    assert isinstance(
        response,
        ReadDataByIdentifierResponse,
    )

    assert response.sid == 0x62
    assert response.did == 0xF190
    assert response.value == b"ABC"


def test_parse_diagnostic_session_control_response() -> None:
    registry = ResponseRegistry()

    registry.register(
        0x50,
        DiagnosticSessionControlResponse,
    )

    parser = UDSResponseParser(
        registry=registry,
    )

    response = parser.parse(
        b"\x50\x03\x00\x32\x13\x88",
    )

    assert isinstance(
        response,
        DiagnosticSessionControlResponse,
    )

    assert response.sid == 0x50
    assert response.session_type == SessionType.EXTENDED
    assert response.p2_server_max == 50
    assert response.p2_star_server_max == 5000


def test_parse_ecu_reset_response() -> None:
    parser = UDSResponseParser(
        registry=ResponseRegistry(),
    )

    response = parser.parse(
        b"\x51\x03",
    )

    assert isinstance(
        response,
        ECUResetResponse,
    )

    assert response.sid == 0x51
    assert response.reset_type == ResetType.SOFT


def test_parse_security_access_response() -> None:
    parser = UDSResponseParser(
        registry=ResponseRegistry(),
    )

    response = parser.parse(
        b"\x67\x01\x12\x34\x56\x78",
    )

    assert isinstance(
        response,
        SecurityAccessResponse,
    )

    assert response.sid == 0x67
    assert response.security_level == SecurityLevel.LEVEL_1_REQUEST_SEED
    assert response.security_data == b"\x12\x34\x56\x78"


def test_parse_read_dtc_information_response() -> None:
    parser = UDSResponseParser(
        registry=ResponseRegistry(),
    )

    response = parser.parse(
        bytes.fromhex("59 02 CF 01 07 00 0F 01 30 00 40"),
    )

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


def test_parse_negative_response() -> None:
    parser = UDSResponseParser(
        registry=ResponseRegistry(),
    )

    response = parser.parse(
        bytes.fromhex("7F 22 31"),
    )

    assert isinstance(response, NegativeResponse)
    assert response.sid == 0x7F
    assert response.original_sid == 0x22
    assert response.response_code == 0x31
