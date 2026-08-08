from opendiag.uds.responses.read_data_by_identifier import (
    ReadDataByIdentifierResponse,
)


def test_create_read_data_by_identifier_response() -> None:
    response = ReadDataByIdentifierResponse(
        sid=0x62,
        did=0xF190,
        value=b"1HGCM82633A004352",
    )

    assert response.sid == 0x62
    assert response.did == 0xF190
    assert response.value == b"1HGCM82633A004352"


def test_create_response_from_bytes() -> None:
    response = ReadDataByIdentifierResponse.from_bytes(
        b"\x62\xf1\x90ABC",
    )

    assert response.sid == 0x62
    assert response.did == 0xF190
    assert response.value == b"ABC"
