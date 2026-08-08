"""
Abstract CAN bus interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from opendiag.core.can_frame import CANFrame


class CANBus(ABC):
    """Abstract interface for CAN bus implementations."""

    @abstractmethod
    def send(self, frame: CANFrame) -> None:
        """Send a CAN frame."""
        raise NotImplementedError

    @abstractmethod
    def receive(
        self,
        timeout: float | None = None,
    ) -> CANFrame | None:
        """Receive a CAN frame."""
        raise NotImplementedError

    @abstractmethod
    def shutdown(self) -> None:
        """Release bus resources."""
        raise NotImplementedError
