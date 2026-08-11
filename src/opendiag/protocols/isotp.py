from __future__ import annotations

import time
from dataclasses import dataclass
from enum import IntEnum

from opendiag.core.can_frame import CANFrame


class FrameType(IntEnum):
    """ISO-TP frame types."""

    SINGLE = 0
    FIRST = 1
    CONSECUTIVE = 2
    FLOW_CONTROL = 3


@dataclass(slots=True)
class ISOTPFrame:
    payload: bytes
    frame_type: FrameType = FrameType.SINGLE
    message_length: int | None = None
    sequence_number: int | None = None

    @property
    def length(self) -> int:
        if self.message_length is not None:
            return self.message_length

        return len(self.payload)

    @classmethod
    def from_can_frame(
        cls,
        frame: CANFrame,
    ) -> ISOTPFrame:
        return cls.from_can_data(
            frame.data,
        )

    @classmethod
    def from_can_data(cls, data: bytes) -> ISOTPFrame:
        pci_type = data[0] >> 4

        # Single Frame
        if pci_type == FrameType.SINGLE.value:
            length = data[0] & 0x0F
            payload = data[1 : 1 + length]

            return cls(
                payload=payload,
                frame_type=FrameType.SINGLE,
            )

        # First Frame
        if pci_type == FrameType.FIRST.value:
            message_length = ((data[0] & 0x0F) << 8) | data[1]
            payload = data[2:]

            return cls(
                payload=payload,
                frame_type=FrameType.FIRST,
                message_length=message_length,
            )

        # Consecutive Frame
        if pci_type == FrameType.CONSECUTIVE.value:
            sequence_number = data[0] & 0x0F
            payload = data[1:]

            return cls(
                payload=payload,
                frame_type=FrameType.CONSECUTIVE,
                sequence_number=sequence_number,
            )

        # Flow Control
        if pci_type == FrameType.FLOW_CONTROL.value:
            return cls(
                payload=b"",
                frame_type=FrameType.FLOW_CONTROL,
            )

        raise NotImplementedError(f"Unsupported ISO-TP PCI type: {pci_type}")

    def to_can_frame(
        self,
        arbitration_id: int,
        is_extended_id: bool = False,
    ) -> CANFrame:
        """Convert an ISO-TP frame into a CAN frame."""

        if self.frame_type is FrameType.SINGLE:
            pci = self.length & 0x0F
            data = bytes([pci]) + self.payload
            return CANFrame(
                arbitration_id=arbitration_id,
                data=data,
                timestamp=0.0,
                is_extended_id=is_extended_id,
            )

        if self.frame_type is FrameType.FIRST:
            if self.message_length is None:
                raise ValueError("First Frame requires message_length")

            pci_high = 0x10 | ((self.message_length >> 8) & 0x0F)
            pci_low = self.message_length & 0xFF

            data = bytes([pci_high, pci_low]) + self.payload

            return CANFrame(
                arbitration_id=arbitration_id,
                data=data,
                timestamp=0.0,
                is_extended_id=is_extended_id,
            )

        if self.frame_type is FrameType.CONSECUTIVE:
            if self.sequence_number is None:
                raise ValueError("Consecutive Frame requires sequence_number")

            pci = 0x20 | (self.sequence_number & 0x0F)

            data = bytes([pci]) + self.payload

            return CANFrame(
                arbitration_id=arbitration_id,
                data=data,
                timestamp=0.0,
                is_extended_id=is_extended_id,
            )

        raise NotImplementedError(f"Unsupported frame type: {self.frame_type}")


@dataclass(slots=True)
class ISOTPMessage:
    """Complete ISO-TP message."""

    payload: bytes


class ISOTPReassembler:
    """Reassembles ISO-TP frames."""

    def __init__(self, timeout: float = 1.0) -> None:
        self._timeout = timeout
        self._reset()

    def _reset(self) -> None:
        """Reset reassembler state."""

        self._buffer = b""
        self._expected_length = 0
        self._next_sequence = 1
        self._start_time = 0.0

    def feed(
        self,
        frame: ISOTPFrame,
    ) -> ISOTPMessage | None:
        """Feed one ISO-TP frame."""

        if frame.frame_type is FrameType.SINGLE:
            return ISOTPMessage(
                payload=frame.payload,
            )

        if frame.frame_type is FrameType.FIRST:
            self._buffer = frame.payload
            self._expected_length = frame.length
            self._next_sequence = 1
            self._start_time = time.monotonic()

            return None

        if frame.frame_type is FrameType.CONSECUTIVE:
            if (time.monotonic() - self._start_time) > self._timeout:
                self._reset()
                raise TimeoutError("ISO-TP reassembly timeout")

            if frame.sequence_number != self._next_sequence:
                self._reset()
                raise ValueError("Invalid ISO-TP sequence number")

            self._buffer += frame.payload

            self._next_sequence = (self._next_sequence + 1) & 0x0F

            if self._next_sequence == 0:
                self._next_sequence = 1

            if len(self._buffer) >= self._expected_length:
                payload = self._buffer[: self._expected_length]

                self._reset()

                return ISOTPMessage(payload=payload)

        return None

        raise NotImplementedError(f"Unsupported frame type: {frame.frame_type}")


class ISOTPSegmenter:
    """Segments ISO-TP messages."""

    def segment(
        self,
        payload: bytes,
    ):
        # Single Frame
        if len(payload) <= 7:
            yield ISOTPFrame(
                payload=payload,
                frame_type=FrameType.SINGLE,
            )
            return

        # First Frame
        yield ISOTPFrame(
            payload=payload[:6],
            frame_type=FrameType.FIRST,
            message_length=len(payload),
        )

        # Consecutive Frames
        sequence_number = 1

        remaining = payload[6:]

        while remaining:
            chunk = remaining[:7]
            remaining = remaining[7:]

            yield ISOTPFrame(
                payload=chunk,
                frame_type=FrameType.CONSECUTIVE,
                sequence_number=sequence_number,
            )

            sequence_number = (sequence_number + 1) & 0x0F

            if sequence_number == 0:
                sequence_number = 1
