from dataclasses import dataclass
from typing import ClassVar

from opendiag.uds.request import UDSRequest


@dataclass(slots=True, frozen=True)
class RequestSeed(UDSRequest):
    """UDS Service 0x27 - Security Access (Request Seed)."""

    SID: ClassVar[int] = 0x27

    level: int

    @property
    def data(self) -> bytes:
        return bytes([self.SID, self.level])


@dataclass(slots=True, frozen=True)
class SendKey(UDSRequest):
    """UDS Service 0x27 - Security Access (Send Key)."""

    SID: ClassVar[int] = 0x27

    level: int
    key: bytes

    @property
    def data(self) -> bytes:
        return bytes([self.SID, self.level]) + self.key
