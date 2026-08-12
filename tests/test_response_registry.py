from opendiag.uds.response import NegativeResponse
from opendiag.uds.response_registry import ResponseRegistry
from opendiag.uds.responses.diagnostic_session_control import (
    DiagnosticSessionControlResponse,
)
from opendiag.uds.responses.read_data_by_identifier import (
    ReadDataByIdentifierResponse,
)
from opendiag.uds.responses.tester_present import (
    TesterPresentResponse,
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


def test_default_registry_contains_read_data_by_identifier() -> None:
    registry = ResponseRegistry()

    assert registry.get(0x62) is ReadDataByIdentifierResponse


def test_default_registry_contains_diagnostic_session_control() -> None:
    registry = ResponseRegistry()

    assert registry.get(0x50) is DiagnosticSessionControlResponse


def test_default_registry_contains_tester_present() -> None:
    registry = ResponseRegistry()

    assert registry.get(0x7E) is TesterPresentResponse


def test_registry_contains_negative_response() -> None:
    registry = ResponseRegistry()

    response_class = registry.get(0x7F)

    assert response_class is NegativeResponse
