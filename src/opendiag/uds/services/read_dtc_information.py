from dataclasses import dataclass
from typing import ClassVar

from opendiag.uds.request import UDSRequest


@dataclass(slots=True, frozen=True)
class ReadDTCInformation(UDSRequest):
    """UDS Service 0x19 - Read DTC Information."""

    SID: ClassVar[int] = 0x19

    subfunction: int
    status_mask: int = 0xFF

    @property
    def data(self) -> bytes:
        return bytes(
            (
                self.SID,
                self.subfunction & 0xFF,
                self.status_mask & 0xFF,
            )
        )
