from dataclasses import dataclass
from typing import ClassVar

from opendiag.uds.request import UDSRequest
from opendiag.uds.reset import ResetType


@dataclass(slots=True, frozen=True)
class ECUReset(UDSRequest):
    """UDS Service 0x11 - ECU Reset."""

    SID: ClassVar[int] = 0x11

    reset_type: ResetType

    @property
    def data(self) -> bytes:
        return bytes([self.SID, self.reset_type])
