from opendiag.uds.response_registry import ResponseRegistry
from opendiag.uds.responses.read_data_by_identifier import (
    ReadDataByIdentifierResponse,
)


def test_register_response() -> None:
    registry = ResponseRegistry()

    registry.register(
        0x62,
        object,
    )

    assert registry.get(0x62) is object


def test_create_registered_response() -> None:
    registry = ResponseRegistry()

    registry.register(
        0x62,
        ReadDataByIdentifierResponse,
    )

    response = registry.create(
        sid=0x62,
        did=0xF190,
        value=b"123456789",
    )

    assert isinstance(
        response,
        ReadDataByIdentifierResponse,
    )

    assert response.did == 0xF190
    assert response.value == b"123456789"
