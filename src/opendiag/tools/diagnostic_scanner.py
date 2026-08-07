"""
Diagnostic Scanner.

Active CAN diagnostic tool.
"""

from __future__ import annotations

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
    ) -> CANFrame:
        """Send a request and wait for a response."""
        self.send(frame)
        return self.receive()
