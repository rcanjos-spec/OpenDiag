from opendiag.uds.response_registry import ResponseRegistry
from opendiag.uds.responses.diagnostic_session_control import (
    DiagnosticSessionControlResponse,
)
from opendiag.uds.responses.ecu_reset import ECUResetResponse
from opendiag.uds.responses.read_data_by_identifier import (
    ReadDataByIdentifierResponse,
)


def register_default_responses(
    registry: ResponseRegistry,
) -> None:
    registry.register(
        0x50,
        DiagnosticSessionControlResponse,
    )

    registry.register(
        0x51,
        ECUResetResponse,
    )

    registry.register(
        0x62,
        ReadDataByIdentifierResponse,
    )
