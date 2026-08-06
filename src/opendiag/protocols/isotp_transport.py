from opendiag.protocols.isotp import (
    ISOTPFrame,
    ISOTPReassembler,
    ISOTPSegmenter,
)


class ISOTPTransport:
    """ISO-TP transport over a CAN bus."""

    def __init__(
        self,
        bus,
        segmenter=None,
        reassembler=None,
        tx_id: int = 0x7E0,
    ) -> None:
        self._bus = bus
        self._segmenter = segmenter or ISOTPSegmenter()
        self._reassembler = reassembler or ISOTPReassembler()
        self._tx_id = tx_id

    def send(
        self,
        data: bytes,
    ) -> None:
        for frame in self._segmenter.segment(data):
            self._bus.send(
                frame.to_can_frame(
                    arbitration_id=self._tx_id,
                )
            )

    def receive(
        self,
    ):
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
