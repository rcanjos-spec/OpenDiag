from collections import deque


class MockTransport:
    def __init__(self) -> None:
        self._responses = deque()
        self.last_request: bytes | None = None

    def queue_response(
        self,
        data: bytes,
    ) -> None:
        self._responses.append(data)

    def send(
        self,
        data: bytes,
    ) -> None:
        self.last_request = data

    def receive(
        self,
    ) -> bytes:
        if not self._responses:
            raise RuntimeError(
                "No queued response available.",
            )

        return self._responses.popleft()
