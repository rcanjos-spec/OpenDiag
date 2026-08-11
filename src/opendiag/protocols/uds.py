class UDSClient:
    """Basic UDS client over an ISO-TP transport."""

    def __init__(self, *, transport) -> None:
        self._transport = transport

    def request(self, request: bytes) -> bytes:
        """Send a UDS request and return the response."""

        self._transport.send(request)

        return self._transport.receive()

    def read_data_by_identifier(self, identifier: int) -> bytes:
        """Read data identified by a UDS data identifier."""

        request = bytes(
            (
                0x22,
                (identifier >> 8) & 0xFF,
                identifier & 0xFF,
            )
        )

        return self.request(request)
