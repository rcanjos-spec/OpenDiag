from __future__ import annotations

from dataclasses import dataclass

from opendiag.uds.response import PositiveResponse
from opendiag.uds.security import SecurityLevel


@dataclass(slots=True, frozen=True, kw_only=True)
class SecurityAccessResponse(PositiveResponse):
    """Positive response for UDS Service 0x27."""

    security_level: SecurityLevel
    security_data: bytes

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
    ) -> SecurityAccessResponse:
        return cls(
            sid=data[0],
            security_level=SecurityLevel(data[1]),
            security_data=data[2:],
        )
