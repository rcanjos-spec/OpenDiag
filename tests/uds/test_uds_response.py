from opendiag.uds.response import NegativeResponse, PositiveResponse, UDSResponse
from opendiag.uds.responses.read_data_by_identifier import (
    ReadDataByIdentifierResponse,
)


def test_create_response() -> None:
    response = UDSResponse(
        sid=0x62,
        payload=b"\xf1\x90",
    )

    assert response.sid == 0x62
    assert response.payload == b"\xf1\x90"


def test_default_payload() -> None:
    response = UDSResponse(
        sid=0x7E,
    )

    assert response.payload == b""


def test_create_positive_response() -> None:
    response = PositiveResponse(
        sid=0x62,
        payload=b"\xf1\x90",
    )

    assert response.sid == 0x62
    assert response.payload == b"\xf1\x90"


def test_create_negative_response() -> None:
    response = NegativeResponse(
        sid=0x7F,
        original_sid=0x22,
        response_code=0x13,
    )

    assert response.sid == 0x7F
    assert response.original_sid == 0x22
    assert response.response_code == 0x13


def test_create_read_data_by_identifier_response() -> None:
    response = ReadDataByIdentifierResponse(
        sid=0x62,
        did=0xF190,
        value=b"1HGCM82633A004352",
    )

    assert response.sid == 0x62
    assert response.did == 0xF190
    assert response.value == b"1HGCM82633A004352"
