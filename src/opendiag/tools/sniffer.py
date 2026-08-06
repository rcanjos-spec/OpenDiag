"""
CAN Sniffer.
"""

from __future__ import annotations

from opendiag.bus.base import CANBus
from opendiag.core.can_frame import CANFrame
from opendiag.logger import Logger
from opendiag.tools.recorder import Recorder


class Sniffer:
    def __init__(
        self,
        bus: CANBus,
        logger: Logger,
        recorder: Recorder | None = None,
    ) -> None:
        self._bus = bus
        self._logger = logger
        self._recorder = recorder

    def receive(self) -> CANFrame:
        frame = self._bus.receive()

        self._logger.can_rx(frame)

        if self._recorder is not None:
            self._recorder.record(frame)

        return frame
