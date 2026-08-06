from dataclasses import dataclass
from typing import ClassVar

from opendiag.uds.request import UDSRequest
from opendiag.uds.response import PositiveResponse


@dataclass(slots=True, frozen=True)
class ReadDataByIdentifier(UDSRequest):
    """UDS Service 0x22 - Read Data By Identifier."""

    SID: ClassVar[int] = 0x22

    did: int

    @property
    def data(self) -> bytes:
        return bytes(
            [
                self.SID,
                (self.did >> 8) & 0xFF,
                self.did & 0xFF,
            ]
        )


@dataclass(slots=True, frozen=True, kw_only=True)
class ReadDataByIdentifierResponse(PositiveResponse):
    """Positive response for UDS Service 0x22."""

    did: int
    value: bytes
