"""
Mock transport implementation.

Provides an in-memory transport used to test protocol layers
without requiring a physical communication interface.
"""

from collections import deque


class MockTransport:
    """
    In-memory transport used for testing.

    Requests sent through the transport are recorded, while responses
    can be queued in advance and returned in the same order.
    """

    def __init__(self) -> None:
        # Stores responses waiting to be returned by receive().
        self._responses = deque()

        # Keeps the most recent request sent by the client.
        self.last_request: bytes | None = None

    def queue_response(
        self,
        data: bytes,
    ) -> None:
        """
        Queue a response for a subsequent receive() call.

        Responses are returned in FIFO order.
        """
        self._responses.append(data)

    def send(
        self,
        data: bytes,
    ) -> None:
        """
        Record the data sent by the client.

        The mock does not transmit anything. It only stores the
        most recent request so tests can verify what was sent.
        """
        self.last_request = data

    def receive(
        self,
    ) -> bytes:
        """
        Return the next queued response.

        Raises RuntimeError when no response has been queued.
        """
        if not self._responses:
            raise RuntimeError(
                "No queued response available.",
            )

        return self._responses.popleft()
