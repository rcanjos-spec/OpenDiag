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

    def read_vin(self) -> str:
        """Read the vehicle VIN using UDS DID F190."""

        response = self.read_data_by_identifier(0xF190)

        if len(response) < 3 or response[:3] != bytes.fromhex("62 F1 90"):
            raise ValueError("Unexpected UDS VIN response")

        vin_bytes = response[3:]

        if len(vin_bytes) != 17:
            raise ValueError("VIN must contain 17 characters")

        try:
            return vin_bytes.decode("ascii")
        except UnicodeDecodeError as exc:
            raise ValueError("VIN must contain ASCII characters") from exc
