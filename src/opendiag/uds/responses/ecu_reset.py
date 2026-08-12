"""
UDS ECU Reset response.

Defines the structured representation of the positive response
returned by the ECU Reset service.
"""

from __future__ import annotations

from dataclasses import dataclass

from opendiag.uds.reset import ResetType
from opendiag.uds.response import PositiveResponse


@dataclass(slots=True, frozen=True, kw_only=True)
class ECUResetResponse(PositiveResponse):
    """
    Positive response for ECU Reset.

    Contains the reset type accepted and returned by the ECU.
    """

    # Reset type reported by the ECU.
    reset_type: ResetType

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
    ) -> ECUResetResponse:
        """
        Decode an ECU Reset positive response.

        Response layout:

            Byte 0: Positive response SID (0x51)
            Byte 1: Reset type
        """
        return cls(
            sid=data[0],
            reset_type=ResetType(data[1]),
        )
