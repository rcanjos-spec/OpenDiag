from dataclasses import dataclass
from typing import ClassVar

from opendiag.uds.request import UDSRequest
from opendiag.uds.session import SessionType


@dataclass(slots=True, frozen=True)
class DiagnosticSessionControl(UDSRequest):
    """UDS Service 0x10 - Diagnostic Session Control."""

    SID: ClassVar[int] = 0x10

    session_type: SessionType

    @property
    def data(self) -> bytes:
        return bytes([self.SID, self.session_type])
