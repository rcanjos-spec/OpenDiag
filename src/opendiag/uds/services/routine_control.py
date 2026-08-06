from dataclasses import dataclass
from typing import ClassVar

from opendiag.uds.request import UDSRequest


@dataclass(slots=True, frozen=True)
class StartRoutine(UDSRequest):
    """UDS Service 0x31 - Routine Control (Start Routine)."""

    SID: ClassVar[int] = 0x31

    routine_id: int

    @property
    def data(self) -> bytes:
        return bytes(
            [
                self.SID,
                0x01,
                (self.routine_id >> 8) & 0xFF,
                self.routine_id & 0xFF,
            ]
        )


@dataclass(slots=True, frozen=True)
class StopRoutine(UDSRequest):
    """UDS Service 0x31 - Routine Control (Stop Routine)."""

    SID: ClassVar[int] = 0x31

    routine_id: int

    @property
    def data(self) -> bytes:
        return bytes(
            [
                self.SID,
                0x02,
                (self.routine_id >> 8) & 0xFF,
                self.routine_id & 0xFF,
            ]
        )


@dataclass(slots=True, frozen=True)
class RequestRoutineResults(UDSRequest):
    """UDS Service 0x31 - Routine Control (Request Routine Results)."""

    SID: ClassVar[int] = 0x31

    routine_id: int

    @property
    def data(self) -> bytes:
        return bytes(
            [
                self.SID,
                0x03,
                (self.routine_id >> 8) & 0xFF,
                self.routine_id & 0xFF,
            ]
        )
