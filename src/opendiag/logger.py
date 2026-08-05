"""
Logging utilities for OpenDiag.
"""

from __future__ import annotations

import logging


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
