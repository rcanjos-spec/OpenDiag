"""
Python-CAN adapter.

Converts between the generic CANFrame representation and the message
format used by python-can.
"""

from __future__ import annotations

import can

from opendiag.bus.base import CANBus
from opendiag.core.can_frame import CANFrame


class PythonCANBus(CANBus):
    """
    CAN bus implementation using python-can.

    This class isolates the python-can dependency from the communication
    layers. Frames entering the class are represented as CANFrame objects,
    while messages sent to the hardware use python-can's Message type.
    """

    def __init__(
        self,
        interface: str,
        channel: str,
        bitrate: int,
        bus: can.BusABC | None = None,
    ) -> None:
        """
        Initialize the CAN adapter.

        A bus instance can be supplied directly, which allows the adapter
        to be tested without creating a physical CAN connection.
        Otherwise, a python-can bus is created from the supplied interface,
        channel, and bitrate configuration.
        """
        self._bus = bus or can.Bus(
            interface=interface,
            channel=channel,
            bitrate=bitrate,
        )

    def send(
        self,
        frame: CANFrame,
    ) -> None:
        """
        Convert a CANFrame into a python-can message and transmit it.

        The adapter is responsible only for translating the internal
        representation into the format expected by the CAN backend.
        """
        message = can.Message(
            arbitration_id=frame.arbitration_id,
            data=frame.data,
            is_extended_id=frame.is_extended_id,
            is_remote_frame=frame.is_remote_frame,
        )

        self._bus.send(message)

    def receive(
        self,
        timeout: float | None = None,
    ) -> CANFrame | None:
        """
        Receive a message and convert it into a CANFrame.

        Returning None when the timeout expires allows upper layers to
        handle the absence of a message without depending on python-can.
        """
        message = self._bus.recv(timeout=timeout)

        if message is None:
            return None

        return CANFrame(
            arbitration_id=message.arbitration_id,
            data=bytes(message.data),
            timestamp=message.timestamp,
            is_extended_id=message.is_extended_id,
            is_remote_frame=message.is_remote_frame,
        )

    def shutdown(self) -> None:
        """
        Release the resources allocated by the CAN backend.
        """
        self._bus.shutdown()
