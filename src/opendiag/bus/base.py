"""
Abstract CAN bus interface.

Defines the contract that every CAN bus implementation must follow.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from opendiag.core.can_frame import CANFrame


class CANBus(ABC):
    """
    Abstract interface for CAN bus implementations.

    This layer separates the communication logic from the physical
    CAN adapter. Concrete implementations are responsible for handling
    the hardware while the upper layers work only with CANFrame objects.
    """

    @abstractmethod
    def send(self, frame: CANFrame) -> None:
        """
        Send a CAN frame through the bus.

        Concrete implementations convert the CANFrame into the format
        required by the underlying CAN interface.
        """
        raise NotImplementedError

    @abstractmethod
    def receive(
        self,
        timeout: float | None = None,
    ) -> CANFrame | None:
        """
        Receive a CAN frame from the bus.

        Returns a CANFrame when a message is received, or None when the
        configured timeout expires without receiving a frame.
        """
        raise NotImplementedError

    @abstractmethod
    def shutdown(self) -> None:
        """
        Release resources associated with the CAN bus.

        Concrete implementations must close the underlying hardware
        interface and release any resources allocated by the adapter.
        """
        raise NotImplementedError
