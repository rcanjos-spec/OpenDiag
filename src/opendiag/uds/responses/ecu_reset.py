from __future__ import annotations

from dataclasses import dataclass

from opendiag.uds.reset import ResetType
from opendiag.uds.response import PositiveResponse


@dataclass(slots=True, frozen=True, kw_only=True)
class ECUResetResponse(PositiveResponse):
    """Positive response for ECU Reset."""

    reset_type: ResetType

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
    ) -> ECUResetResponse:
        return cls(
            sid=data[0],
            reset_type=ResetType(data[1]),
        )
