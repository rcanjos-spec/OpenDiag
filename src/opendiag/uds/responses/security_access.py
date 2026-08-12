"""
UDS Security Access response.

Defines the structured representation of the positive response
returned by the Security Access service.
"""

from __future__ import annotations

from dataclasses import dataclass

from opendiag.uds.response import PositiveResponse
from opendiag.uds.security import SecurityLevel


@dataclass(slots=True, frozen=True, kw_only=True)
class SecurityAccessResponse(PositiveResponse):
    """
    Positive response for UDS Service 0x27.

    Contains the security access subfunction and the security data
    returned by the diagnostic server.
    """

    # Security access level returned by the server.
    security_level: SecurityLevel

    # Seed or security data associated with the requested security level.
    security_data: bytes

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
    ) -> SecurityAccessResponse:
        """
        Decode a Security Access positive response.

        Response layout:

            Byte 0: Positive response SID (0x67)
            Byte 1: Security access level
            Remaining bytes: Security data
        """
        return cls(
            sid=data[0],
            security_level=SecurityLevel(data[1]),
            security_data=data[2:],
        )
