"""
CAN frame representation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CANFrame:
    """Represents a classical CAN frame."""

    arbitration_id: int
    data: bytes
    timestamp: float

    is_extended_id: bool = False
    is_remote_frame: bool = False

    @property
    def dlc(self) -> int:
        """Return the Data Length Code (DLC)."""
        return len(self.data)
