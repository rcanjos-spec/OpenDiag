"""
OBD-II diagnostic client.

Provides VIN parsing and the request flow required to retrieve
the vehicle identification number through Mode 09 PID 02.
"""


def parse_vin(response: bytes) -> str:
    """
    Parse an OBD-II Mode 09 PID 02 VIN response.

    The response must contain the expected service, PID, and frame
    identifier followed by exactly 17 ASCII characters.
    """
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
    """
    Coordinates OBD-II diagnostic requests.

    The client delegates transport operations to the configured
    transport and handles the interpretation of the returned data.
    """

    def __init__(self, *, transport) -> None:
        """
        Initialize the OBD-II client with a transport implementation.
        """
        self._transport = transport

    def read_vin(self) -> str:
        """
        Request and decode the vehicle VIN using Mode 09 PID 02.
        """
        self._transport.send(
            b"\x09\x02",
        )

        response = self._transport.receive()

        return parse_vin(response)
