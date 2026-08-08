from opendiag.uds.request import UDSRequest
from opendiag.uds.reset import ResetType
from opendiag.uds.security import SecurityLevel
from opendiag.uds.services.ecu_reset import ECUReset
from opendiag.uds.services.security_access import SecurityAccess
from opendiag.uds.services.tester_present import TesterPresent


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
        request = TesterPresent()

        self._transport.send(
            request.data,
        )

        response = self._transport.receive()

        return self._parser.parse(response)

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
