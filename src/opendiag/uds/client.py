class UDSClient:
    def __init__(
        self,
        transport,
        registry,
    ):
        self._transport = transport
        self._registry = registry
