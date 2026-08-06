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
        bus: can.BusABC | None = None,
    ) -> None:
        self._bus = bus or can.Bus(
            interface=interface,
            channel=channel,
            bitrate=bitrate,
        )

    def send(
        self,
        frame: CANFrame,
    ) -> None:
        message = can.Message(
            arbitration_id=frame.arbitration_id,
            data=frame.data,
            is_extended_id=frame.is_extended_id,
            is_remote_frame=frame.is_remote_frame,
        )

        self._bus.send(message)

    def receive(
        self,
    ) -> CANFrame:
        message = self._bus.recv()

        return CANFrame(
            arbitration_id=message.arbitration_id,
            data=bytes(message.data),
            timestamp=message.timestamp,
            is_extended_id=message.is_extended_id,
            is_remote_frame=message.is_remote_frame,
        )

    def shutdown(self) -> None:
        self._bus.shutdown()
