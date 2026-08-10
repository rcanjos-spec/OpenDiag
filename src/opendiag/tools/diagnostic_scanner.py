"""
Diagnostic Scanner.

Active CAN diagnostic tool.
"""

from __future__ import annotations

import time
from collections.abc import Callable

from opendiag.bus.base import CANBus
from opendiag.core.can_frame import CANFrame


class DiagnosticScanner:
    """Active CAN diagnostic tool."""

    def __init__(
        self,
        bus: CANBus,
    ) -> None:
        self._bus = bus

    def send(
        self,
        frame: CANFrame,
    ) -> None:
        """Send a CAN frame."""
        self._bus.send(frame)

    def receive(
        self,
        timeout: float | None = None,
    ) -> CANFrame | None:
        """Receive a CAN frame."""

        if timeout is None:
            return self._bus.receive()

        return self._bus.receive(
            timeout=timeout,
        )

    def scan(
        self,
        duration: float,
    ) -> dict[int, int]:
        """Scan the CAN bus and count frames by arbitration ID."""

        counts: dict[int, int] = {}
        deadline = time.monotonic() + duration

        while True:
            remaining = deadline - time.monotonic()

            if remaining <= 0:
                break

            frame = self.receive(
                timeout=remaining,
            )

            if frame is None:
                break

            counts[frame.arbitration_id] = counts.get(frame.arbitration_id, 0) + 1

        return counts

    def capture(
        self,
        duration: float,
    ) -> list[CANFrame]:
        """Capture CAN frames for a fixed duration."""

        frames: list[CANFrame] = []
        deadline = time.monotonic() + duration

        while True:
            remaining = deadline - time.monotonic()

            if remaining <= 0:
                break

            frame = self.receive(
                timeout=remaining,
            )

            if frame is None:
                break

            frames.append(frame)

        return frames

    def request(
        self,
        frame: CANFrame,
        *,
        response_filter: Callable[[CANFrame], bool],
        timeout: float = 3.0,
    ) -> CANFrame:
        """Send a request and wait for the expected response."""

        self.send(frame)

        deadline = time.monotonic() + timeout

        while True:
            remaining = deadline - time.monotonic()

            if remaining <= 0:
                raise TimeoutError

            response = self.receive(
                timeout=remaining,
            )

            if response is None:
                continue

            if response_filter(response):
                return response
