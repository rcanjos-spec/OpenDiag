"""
Frame formatting utilities.
"""

from __future__ import annotations

from opendiag.core.can_frame import CANFrame


class FrameFormatter:
    """Formats CAN frames for display."""

    @staticmethod
    def format(frame: CANFrame) -> str:
        data = " ".join(f"{byte:02X}" for byte in frame.data)
        return f"{frame.arbitration_id:X} [{frame.dlc}] {data}"
