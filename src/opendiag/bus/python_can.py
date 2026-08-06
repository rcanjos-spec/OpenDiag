"""
Python-CAN adapter.
"""

from __future__ import annotations

import can

from opendiag.bus.base import CANBus
from opendiag.core.can_frame import CANFrame


class PythonCANBus(CANBus):
    """CAN bus implementation using python-can."""

    def __init__(
        self,
        interface: str,
        channel: str,
        bitrate: int,
    ) -> None:
        self._bus = can.Bus(
            interface=interface,
            channel=channel,
            bitrate=bitrate,
        )

    def send(self, frame: CANFrame) -> None:
        raise NotImplementedError

    def receive(self) -> CANFrame:
        raise NotImplementedError

    def shutdown(self) -> None:
        self._bus.shutdown()
