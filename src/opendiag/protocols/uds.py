from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UDSNegativeResponse:
    """Represents a UDS negative response."""

    service_id: int
    nrc: int

    @property
    def nrc_description(self) -> str:
        """Return a human-readable description for the NRC."""

        descriptions = {
            0x10: "GeneralReject",
            0x11: "ServiceNotSupported",
            0x12: "SubFunctionNotSupported",
            0x13: "IncorrectMessageLengthOrInvalidFormat",
            0x22: "ConditionsNotCorrect",
            0x31: "RequestOutOfRange",
            0x33: "SecurityAccessDenied",
            0x35: "InvalidKey",
            0x78: "ResponsePending",
        }

        return descriptions.get(
            self.nrc,
            "UnknownNRC",
        )


class UDSClient:
    """Basic UDS client over an ISO-TP transport."""

    @staticmethod
    def parse_negative_response(response: bytes) -> UDSNegativeResponse:
        """Parse a UDS negative response."""

        if len(response) != 3 or response[0] != 0x7F:
            raise ValueError("Invalid UDS negative response")

        return UDSNegativeResponse(
            service_id=response[1],
            nrc=response[2],
        )

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

        return self.request_positive(request)

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

    def start_diagnostic_session(self, session: int) -> bytes:
        """Start a UDS diagnostic session."""

        request = bytes(
            (
                0x10,
                session & 0xFF,
            )
        )

        return self.request_positive(request)

    def request_positive(self, request: bytes) -> bytes:
        """Send a UDS request and reject negative responses."""

        response = self.request(request)

        if response and response[0] == 0x7F:
            negative = self.parse_negative_response(response)

            raise ValueError(
                f"Negative UDS response: "
                f"service=0x{negative.service_id:02X}, "
                f"nrc=0x{negative.nrc:02X} "
                f"({negative.nrc_description})"
            )

        return response
