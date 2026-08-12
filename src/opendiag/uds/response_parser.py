"""
UDS response parser.

Converts raw UDS response bytes into the response type registered
for the corresponding service identifier.
"""


class UDSResponseParser:
    """
    Parses raw UDS responses using a response registry.

    The parser does not contain service-specific decoding logic.
    Instead, it uses the registry to locate the response class
    responsible for interpreting the received data.
    """

    def __init__(
        self,
        registry,
    ) -> None:
        """
        Initialize the parser with a response registry.

        The registry provides the association between a UDS response
        SID and the class responsible for parsing that response.
        """
        self._registry = registry

    def parse(
        self,
        data: bytes,
    ):
        """
        Parse a raw UDS response.

        The first byte identifies the response service. The registry
        is then used to select the appropriate response class, which
        performs the service-specific decoding.
        """
        sid = data[0]

        response_class = self._registry.get(sid)

        return response_class.from_bytes(data)
