import time
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


class UDSNegativeResponseError(ValueError):
    """Raised when the ECU returns a UDS negative response."""

    def __init__(
        self,
        response: UDSNegativeResponse,
    ) -> None:
        self.service_id = response.service_id
        self.nrc = response.nrc
        self.nrc_description = response.nrc_description

        super().__init__(
            f"Negative UDS response: "
            f"service=0x{self.service_id:02X}, "
            f"nrc=0x{self.nrc:02X} "
            f"({self.nrc_description})"
        )


@dataclass(frozen=True, slots=True)
class UDSDTC:
    """Represents a UDS diagnostic trouble code."""

    code: int
    status: int


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

    def receive(self, timeout: float | None = None) -> bytes:
        """Receive a UDS response from the transport."""

        return self._transport.receive(timeout=timeout)

    def request_positive(
        self,
        request: bytes,
        timeout: float = 1.0,
    ) -> bytes:
        """Send a UDS request and wait for a positive response."""

        self._transport.send(request)

        deadline = time.monotonic() + timeout

        while True:
            remaining = deadline - time.monotonic()

            if remaining <= 0:
                raise TimeoutError("UDS response pending timeout")

            response = self.receive(timeout=remaining)

            if response and response[0] == 0x7F:
                negative = self.parse_negative_response(response)

                if negative.nrc == 0x78:
                    continue

                raise UDSNegativeResponseError(negative)

            return response

    def read_dtc_information(self, subfunction: int) -> list[UDSDTC]:
        """Read diagnostic trouble code information."""

        request = bytes(
            (
                0x19,
                subfunction & 0xFF,
            )
        )

        response = self.request_positive(request)

        return self.parse_dtc_information(response)

    @staticmethod
    def parse_dtc_information(response: bytes) -> list[UDSDTC]:
        """Parse a UDS ReadDTCInformation response."""

        if len(response) < 2 or response[:2] != bytes.fromhex("59 02"):
            raise ValueError("Invalid UDS DTC response")

        payload = response[2:]

        if len(payload) % 4 != 0:
            raise ValueError("Invalid UDS DTC response")

        dtcs = []

        for offset in range(0, len(payload), 4):
            code = int.from_bytes(
                payload[offset : offset + 3],
                byteorder="big",
            )
            status = payload[offset + 3]

            dtcs.append(
                UDSDTC(
                    code=code,
                    status=status,
                )
            )

        return dtcs
