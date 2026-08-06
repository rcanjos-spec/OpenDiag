from dataclasses import dataclass

from opendiag.uds.response import PositiveResponse


@dataclass(slots=True, frozen=True, kw_only=True)
class DiagnosticSessionControlResponse(PositiveResponse):
    """Positive response for UDS Service 0x10."""

    session_type: int

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
    ) -> DiagnosticSessionControlResponse:
        return cls(
            sid=data[0],
            session_type=data[1],
        )
