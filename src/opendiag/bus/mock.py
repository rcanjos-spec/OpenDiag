"""
Mock CAN bus implementation.

Provides an in-memory CAN bus used to exercise communication logic
without requiring physical CAN hardware.
"""

from __future__ import annotations

from collections import deque

from opendiag.bus.base import CANBus
from opendiag.core.can_frame import CANFrame
from opendiag.core.exceptions import BusError


class MockCANBus(CANBus):
    """
    In-memory CAN bus implementation for testing.

    Frames are stored in a FIFO queue. This allows tests to simulate
    CAN transmission and reception while using the same CANBus
    interface as the physical adapter.
    """

    def __init__(self) -> None:
        """
        Initialize an empty frame queue.

        The queue provides deterministic FIFO behavior for simulated
        CAN communication.
        """
        self._queue: deque[CANFrame] = deque()

    def send(self, frame: CANFrame) -> None:
        """
        Store a CAN frame in the internal queue.

        In the mock implementation, sending a frame makes it available
        to receive(), simulating a loopback-style communication path.
        """
        self._queue.append(frame)

    def receive(self) -> CANFrame:
        """
        Return the oldest frame in the queue.

        Raises:
            BusError: If no frame is currently available.
        """
        if not self._queue:
            raise BusError("No CAN frames available.")

        return self._queue.popleft()

    def shutdown(self) -> None:
        """
        Clear the simulated bus and release its queued frames.
        """
        self._queue.clear()
