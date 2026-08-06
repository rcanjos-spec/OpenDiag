class ResponseRegistry:
    def __init__(self) -> None:
        self._responses = {}

    def register(
        self,
        sid: int,
        response,
    ) -> None:
        self._responses[sid] = response

    def get(
        self,
        sid: int,
    ):
        return self._responses[sid]

    def create(
        self,
        sid: int,
        **kwargs,
    ):
        response_class = self.get(sid)

        return response_class(
            sid=sid,
            **kwargs,
        )
