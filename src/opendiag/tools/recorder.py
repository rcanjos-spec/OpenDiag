"""
CAN frame recorder.
"""

from pathlib import Path

from opendiag.core.can_frame import CANFrame
from opendiag.utils.frame_formatter import FrameFormatter


class Recorder:
    """Records CAN frames to a text file."""

    def __init__(self, filename: Path | str) -> None:
        self._filename = Path(filename)

    def record(self, frame: CANFrame) -> None:
        """Append one CAN frame to the log file."""

        with self._filename.open("a", encoding="utf-8") as file:
            file.write(FrameFormatter.format(frame) + "\n")
