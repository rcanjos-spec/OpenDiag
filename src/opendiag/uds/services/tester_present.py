from dataclasses import dataclass
from typing import ClassVar

from opendiag.uds.constants import TESTER_PRESENT
from opendiag.uds.request import UDSRequest


@dataclass(slots=True, frozen=True)
class TesterPresent(UDSRequest):
    """UDS Service 0x3E - Tester Present."""

    SID: ClassVar[int] = TESTER_PRESENT

    suppress_response: bool = False

    @property
    def data(self) -> bytes:
        sub_function = 0x80 if self.suppress_response else 0x00
        return bytes([self.SID, sub_function])
