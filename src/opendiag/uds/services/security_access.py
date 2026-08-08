from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from opendiag.uds.request import UDSRequest
from opendiag.uds.security import SecurityLevel


@dataclass(slots=True, frozen=True)
class SecurityAccess(UDSRequest):
    """UDS Service 0x27 - Security Access."""

    SID: ClassVar[int] = 0x27

    level: SecurityLevel
    key: bytes = b""

    @property
    def data(self) -> bytes:
        return (
            bytes(
                (
                    self.SID,
                    self.level,
                )
            )
            + self.key
        )
