class UDSResponseParser:
    def __init__(
        self,
        registry,
    ) -> None:
        self._registry = registry

    def parse(
        self,
        data: bytes,
    ):
        sid = data[0]

        response_class = self._registry.get(sid)

        return response_class.from_bytes(data)
