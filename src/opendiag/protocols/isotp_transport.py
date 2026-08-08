from opendiag.protocols.isotp import (
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
    ) -> None:
        self._bus = bus
        self._scanner = scanner
        self._segmenter = segmenter or ISOTPSegmenter()
        self._reassembler = reassembler or ISOTPReassembler()
        self._tx_id = tx_id

    def send(
        self,
        data: bytes,
    ) -> None:
        for frame in self._segmenter.segment(data):
            can_frame = frame.to_can_frame(
                arbitration_id=self._tx_id,
            )

            if self._scanner is not None:
                self._scanner.send(can_frame)
            else:
                self._bus.send(can_frame)

    def receive(
        self,
    ):
        if self._scanner is not None:
            can_frame = self._scanner.receive()
        else:
            can_frame = self._bus.receive()

        frame = ISOTPFrame.from_can_frame(
            can_frame,
        )

        message = self._reassembler.feed(
            frame,
        )

        if message is None:
            return None

        return message.payload
