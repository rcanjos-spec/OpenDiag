from dataclasses import dataclass

from opendiag.uds.response import PositiveResponse
from opendiag.uds.session import SessionType


@dataclass(slots=True, frozen=True, kw_only=True)
class DiagnosticSessionControlResponse(PositiveResponse):
    """Positive response for Diagnostic Session Control."""

    session_type: SessionType
    p2_server_max: int
    p2_star_server_max: int

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
    ) -> DiagnosticSessionControlResponse:
        return cls(
            sid=data[0],
            session_type=SessionType(data[1]),
            p2_server_max=int.from_bytes(data[2:4], "big"),
            p2_star_server_max=int.from_bytes(data[4:6], "big"),
        )
