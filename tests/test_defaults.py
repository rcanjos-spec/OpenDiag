from opendiag.uds.defaults import register_default_responses
from opendiag.uds.response_registry import ResponseRegistry
from opendiag.uds.responses.diagnostic_session_control import (
    DiagnosticSessionControlResponse,
)
from opendiag.uds.responses.ecu_reset import ECUResetResponse
from opendiag.uds.responses.read_data_by_identifier import (
    ReadDataByIdentifierResponse,
)


def test_register_default_responses() -> None:
    registry = ResponseRegistry()

    register_default_responses(
        registry,
    )

    assert registry.get(0x50) is DiagnosticSessionControlResponse
    assert registry.get(0x51) is ECUResetResponse
    assert registry.get(0x62) is ReadDataByIdentifierResponse
