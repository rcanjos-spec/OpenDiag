from opendiag.uds.request import UDSRequest
from opendiag.uds.reset import ResetType
from opendiag.uds.security import SecurityLevel
from opendiag.uds.services.diagnostic_session_control import (
    DiagnosticSessionControl,
)
from opendiag.uds.services.ecu_reset import ECUReset
from opendiag.uds.services.read_data_by_identifier import (
    ReadDataByIdentifier,
)
from opendiag.uds.services.read_dtc_information import (
    ReadDTCInformation,
)
from opendiag.uds.services.security_access import SecurityAccess
from opendiag.uds.services.tester_present import TesterPresent
from opendiag.uds.session import SessionType


class UDSClient:
    """Coordinates the UDS request/response workflow.

    Responsibilities:
    - send serialized requests through the transport;
    - receive raw responses;
    - delegate response parsing to the parser;
    - return the parsed response.
    """

    def __init__(
        self,
        *,
        transport=None,
        scanner=None,
        parser,
    ) -> None:
        self._transport = transport
        self._scanner = scanner
        self._parser = parser

    def read_data_by_identifier(
        self,
        did: int,
    ):
        """Read data by identifier using UDS service 0x22."""

        return self.send(
            ReadDataByIdentifier(
                did=did,
            )
        )

    def read_vin(self) -> str:
        """Read the vehicle VIN using UDS DID F190."""

        response = self.read_data_by_identifier(0xF190)

        if len(response.value) != 17:
            raise ValueError("VIN must contain 17 characters")

        try:
            return response.value.decode("ascii")
        except UnicodeDecodeError as exc:
            raise ValueError("VIN must contain ASCII characters") from exc

    def read_dtc_information(
        self,
        subfunction: int = 0x02,
        status_mask: int = 0xFF,
    ):
        """Read diagnostic trouble code information."""

        return self.send(
            ReadDTCInformation(
                subfunction=subfunction,
                status_mask=status_mask,
            )
        )

    def send(
        self,
        request: UDSRequest,
    ):
        if self._scanner is not None:
            response = self._scanner.request(
                request.data,
            )

            return self._parser.parse(response.data)

        self._transport.send(request.data)

        response = self._transport.receive()

        return self._parser.parse(response)

    def tester_present(
        self,
    ):
        """Send Tester Present request."""

        return self.send(
            TesterPresent(),
        )

    def diagnostic_session_control(
        self,
        session_type: SessionType = SessionType.DEFAULT,
    ):
        """Change the ECU diagnostic session."""

        return self.send(
            DiagnosticSessionControl(
                session_type=session_type,
            )
        )

    def ecu_reset(
        self,
        reset_type: ResetType = ResetType.HARD,
    ):
        """Send ECU Reset request."""

        return self.send(
            ECUReset(
                reset_type=reset_type,
            )
        )

    def security_access(
        self,
        level: SecurityLevel,
        key: bytes = b"",
    ):
        """Send Security Access request."""

        return self.send(
            SecurityAccess(
                level=level,
                key=key,
            )
        )
