from opendiag.uds.response_parser import UDSResponseParser
from opendiag.uds.response_registry import ResponseRegistry
from opendiag.uds.responses.read_data_by_identifier import (
    ReadDataByIdentifierResponse,
)


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
