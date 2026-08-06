from opendiag.transport import Transport
from opendiag.uds.request import UDSRequest
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
        transport: Transport,
        parser,
    ) -> None:
        self._transport = transport
        self._parser = parser

    def send(
        self,
        request: UDSRequest,
    ):
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

        return self._parser.parse(
            response,
        )
