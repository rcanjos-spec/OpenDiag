class UDSClient:
    """Basic UDS client over an ISO-TP transport."""

    def __init__(self, *, transport) -> None:
        self._transport = transport

    def request(self, request: bytes) -> bytes:
        """Send a UDS request and return the response."""

        self._transport.send(request)

        return self._transport.receive()
