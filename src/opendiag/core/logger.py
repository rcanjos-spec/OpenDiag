"""
Logging utilities for OpenDiag.
"""

from __future__ import annotations

import logging

from opendiag.core.can_frame import CANFrame
from opendiag.utils.frame_formatter import FrameFormatter


class OpenDiagLogger:
    """Wrapper around the standard Python logger."""

    def __init__(self, name: str = "OpenDiag") -> None:
        self._logger = logging.getLogger(name)

        if not self._logger.handlers:
            handler = logging.StreamHandler()

            formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

            handler.setFormatter(formatter)

            self._logger.addHandler(handler)

            self._logger.setLevel(logging.INFO)

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def critical(self, message: str) -> None:
        self._logger.critical(message)

    def can_rx(self, frame: CANFrame) -> None:
        """Log a received CAN frame."""
        self.info(f"CAN RX | {FrameFormatter.format(frame)}")

    def can_tx(self, frame: CANFrame) -> None:
        """Log a transmitted CAN frame."""
        self.info(f"CAN TX | {FrameFormatter.format(frame)}")
