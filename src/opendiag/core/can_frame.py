"""
CAN frame representation.

Defines the internal representation of a CAN message used by the
communication layers.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CANFrame:
    """
    Represents a classical CAN frame.

    This class provides a hardware-independent representation of a CAN
    message. Hardware adapters convert their native message format into
    CANFrame before passing it to the communication layers.
    """

    # CAN arbitration identifier used to identify the message.
    arbitration_id: int

    # Raw CAN payload received from or sent to the bus.
    data: bytes

    # Timestamp associated with the frame.
    timestamp: float

    # Indicates whether the frame uses the 29-bit extended identifier.
    is_extended_id: bool = False

    # Indicates whether the frame is a Remote Transmission Request.
    is_remote_frame: bool = False

    @property
    def dlc(self) -> int:
        """
        Return the number of bytes contained in the CAN payload.

        The DLC is derived from the payload instead of being stored
        separately, preventing the two values from becoming inconsistent.
        """
        return len(self.data)
