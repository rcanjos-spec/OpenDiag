"""
Mock CAN bus implementation.
"""

from __future__ import annotations

from collections import deque

from opendiag.bus.base import CANBus
from opendiag.core.can_frame import CANFrame
from opendiag.core.exceptions import BusError


class MockCANBus(CANBus):
    """Mock implementation of a CAN bus for testing."""

    def __init__(self) -> None:
        self._queue: deque[CANFrame] = deque()

    def send(self, frame: CANFrame) -> None:
        self._queue.append(frame)

    def receive(self) -> CANFrame:
        if not self._queue:
            raise BusError("No CAN frames available.")

        return self._queue.popleft()

    def shutdown(self) -> None:
        self._queue.clear()
