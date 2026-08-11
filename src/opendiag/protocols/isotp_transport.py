import time

from opendiag.core.can_frame import CANFrame
from opendiag.protocols.isotp import (
    FrameType,
    ISOTPFrame,
    ISOTPReassembler,
    ISOTPSegmenter,
)


class ISOTPTransport:
    """ISO-TP transport over a CAN bus."""

    def __init__(
        self,
        *,
        bus=None,
        scanner=None,
        segmenter=None,
        reassembler=None,
        tx_id: int = 0x7E0,
        tx_extended: bool = False,
        rx_id: int | None = None,
        flow_control_id: int | None = None,
    ) -> None:
        self._bus = bus
        self._scanner = scanner
        self._segmenter = segmenter or ISOTPSegmenter()
        self._reassembler = reassembler or ISOTPReassembler()
        self._tx_id = tx_id
        self._tx_extended = tx_extended
        self._rx_id = rx_id
        self._flow_control_id = (
            flow_control_id if flow_control_id is not None else tx_id
        )

    def send(
        self,
        data: bytes,
    ) -> None:
        for frame in self._segmenter.segment(data):
            if self._tx_extended:
                can_frame = frame.to_can_frame(
                    arbitration_id=self._tx_id,
                    is_extended_id=True,
                )
            else:
                can_frame = frame.to_can_frame(
                    arbitration_id=self._tx_id,
                )

            if self._scanner is not None:
                self._scanner.send(can_frame)
            else:
                self._bus.send(can_frame)

    def receive(
        self,
        timeout: float | None = None,
    ):
        deadline = None if timeout is None else time.monotonic() + timeout

        while True:
            if deadline is None:
                remaining = None
            else:
                remaining = deadline - time.monotonic()

                if remaining <= 0:
                    raise TimeoutError("ISO-TP receive timeout")

            if self._scanner is not None:
                can_frame = self._scanner.receive(
                    timeout=remaining,
                )
            else:
                can_frame = self._bus.receive(
                    timeout=remaining,
                )

            if can_frame is None:
                raise TimeoutError("ISO-TP receive timeout")

            if self._rx_id is not None and can_frame.arbitration_id != self._rx_id:
                continue

            frame = ISOTPFrame.from_can_frame(
                can_frame,
            )

            if frame.frame_type is FrameType.FIRST:
                flow_control = CANFrame(
                    arbitration_id=self._flow_control_id,
                    data=bytes.fromhex("30 00 00 00 00 00 00 00"),
                    timestamp=0.0,
                    is_extended_id=self._tx_extended,
                )

                if self._scanner is not None:
                    self._scanner.send(flow_control)
                else:
                    self._bus.send(flow_control)

            message = self._reassembler.feed(
                frame,
            )

            if message is not None:
                return message.payload
                if self._scanner is not None:
                    self._scanner.send(flow_control)
                else:
                    self._bus.send(flow_control)

                message = self._reassembler.feed(
                    frame,
                )

                if message is not None:
                    return message.payload
