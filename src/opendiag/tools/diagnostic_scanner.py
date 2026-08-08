"""
Diagnostic Scanner.

Active CAN diagnostic tool.
"""

from __future__ import annotations

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

    def receive(self) -> CANFrame:
        """Receive a CAN frame."""
        return self._bus.receive()

    def request(
        self,
        frame: CANFrame,
        *,
        response_filter: Callable[[CANFrame], bool],
        timeout: int = 3,
    ) -> CANFrame:
        """Send a request and wait for the expected response."""

        self.send(frame)

        attempts = 0

        while True:
            response = self.receive()

            if response is None:
                attempts += 1

                if attempts >= timeout:
                    raise TimeoutError

                continue

            if response_filter(response):
                return response
