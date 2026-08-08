from opendiag.uds.responses.diagnostic_session_control import (
    DiagnosticSessionControlResponse,
)
from opendiag.uds.responses.ecu_reset import ECUResetResponse
from opendiag.uds.responses.read_data_by_identifier import (
    ReadDataByIdentifierResponse,
)
from opendiag.uds.responses.security_access import (
    SecurityAccessResponse,
)


class ResponseRegistry:
    def __init__(self) -> None:
        self._responses = {}

        self.register(
            0x51,
            ECUResetResponse,
        )
        self.register(
            0x50,
            DiagnosticSessionControlResponse,
        )

        self.register(
            0x62,
            ReadDataByIdentifierResponse,
        )

        self.register(
            0x67,
            SecurityAccessResponse,
        )

    def register(
        self,
        sid: int,
        response,
    ) -> None:
        self._responses[sid] = response

    def get(
        self,
        sid: int,
    ):
        return self._responses[sid]

    def create(
        self,
        sid: int,
        **kwargs,
    ):
        response_class = self.get(sid)

        return response_class(
            sid=sid,
            **kwargs,
        )
