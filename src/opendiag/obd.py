def parse_vin(response: bytes) -> str:
    """Parse an OBD-II Mode 09 PID 02 VIN response."""

    if len(response) < 4 or response[0:3] != bytes((0x49, 0x02, 0x01)):
        raise ValueError("Unexpected OBD response")

    vin_bytes = response[3:]

    if len(vin_bytes) != 17:
        raise ValueError("VIN must contain 17 characters")

    try:
        vin = vin_bytes.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ValueError("VIN must contain ASCII characters") from exc

    return vin


class OBDClient:
    """Coordinates OBD-II diagnostic requests."""

    def __init__(self, *, transport) -> None:
        self._transport = transport

    def read_vin(self) -> str:
        """Read the vehicle VIN using OBD-II Mode 09 PID 02."""

        self._transport.send(
            b"\x09\x02",
        )

        response = self._transport.receive()

        return parse_vin(response)
