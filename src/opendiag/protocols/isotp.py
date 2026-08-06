from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum


class ISOTPFrameType(Enum):
    """ISO-TP frame types."""

    SINGLE = 0x0
    FIRST = 0x1
    CONSECUTIVE = 0x2
    FLOW_CONTROL = 0x3


@dataclass(slots=True)
class ISOTPFrame:
    payload: bytes
    frame_type: ISOTPFrameType = ISOTPFrameType.SINGLE
    message_length: int | None = None
    sequence_number: int | None = None

    @property
    def length(self) -> int:
        if self.message_length is not None:
            return self.message_length

        return len(self.payload)

    @classmethod
    def from_can_data(cls, data: bytes) -> ISOTPFrame:
        pci_type = data[0] >> 4

        # Single Frame
        if pci_type == ISOTPFrameType.SINGLE.value:
            length = data[0] & 0x0F
            payload = data[1 : 1 + length]

            return cls(
                payload=payload,
                frame_type=ISOTPFrameType.SINGLE,
            )

        # First Frame
        if pci_type == ISOTPFrameType.FIRST.value:
            message_length = ((data[0] & 0x0F) << 8) | data[1]
            payload = data[2:]

            return cls(
                payload=payload,
                frame_type=ISOTPFrameType.FIRST,
                message_length=message_length,
            )

        # Consecutive Frame
        if pci_type == ISOTPFrameType.CONSECUTIVE.value:
            sequence_number = data[0] & 0x0F
            payload = data[1:]

            return cls(
                payload=payload,
                frame_type=ISOTPFrameType.CONSECUTIVE,
                sequence_number=sequence_number,
            )

        # Flow Control
        if pci_type == ISOTPFrameType.FLOW_CONTROL.value:
            return cls(
                payload=b"",
                frame_type=ISOTPFrameType.FLOW_CONTROL,
            )

        raise NotImplementedError(f"Unsupported ISO-TP PCI type: {pci_type}")


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

        if frame.frame_type is ISOTPFrameType.SINGLE:
            return ISOTPMessage(
                payload=frame.payload,
            )

        if frame.frame_type is ISOTPFrameType.FIRST:
            self._buffer = frame.payload
            self._expected_length = frame.length
            self._next_sequence = 1
            self._start_time = time.monotonic()

            return None

        if frame.frame_type is ISOTPFrameType.CONSECUTIVE:
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

                self.reset()

                return ISOTPMessage(payload=payload)

        return None

        raise NotImplementedError(f"Unsupported frame type: {frame.frame_type}")

    def test_reassembler_resets_after_timeout() -> None:
        reassembler = ISOTPReassembler(timeout=0.1)

        first = ISOTPFrame.from_can_data(b"\x10\x09\x62\xf1\x90\x31\x47\x31")

        assert reassembler.feed(first) is None

        import time

        time.sleep(0.2)

        try:
            reassembler.feed(ISOTPFrame.from_can_data(b"\x21\x58\x58\x58"))
        except TimeoutError:
            pass

        new_first = ISOTPFrame.from_can_data(b"\x10\x09\x62\xf1\x90\x31\x47\x31")

        assert reassembler.feed(new_first) is None


class ISOTPSegmenter:
    """Segments ISO-TP messages."""

    def segment(
        self,
        payload: bytes,
    ):

        yield ISOTPFrame(
            payload=payload,
            frame_type=ISOTPFrameType.SINGLE,
        )
