from opendiag.protocols.isotp import (
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
    ) -> None:
        self._bus = bus
        self._segmenter = segmenter or ISOTPSegmenter()
        self._reassembler = reassembler or ISOTPReassembler()

    def send(
        self,
        data: bytes,
    ) -> None:
        for frame in self._segmenter.segment(data):
            self._bus.send(frame)

    def receive(
        self,
    ):
        frame = self._bus.receive()

        return self._reassembler.feed(frame)
