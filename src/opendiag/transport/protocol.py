from typing import Protocol


class Transport(Protocol):
    """Transport abstraction used by UDSClient."""

    def send(self, data: bytes) -> None:
        """Send raw bytes."""
        ...

    def receive(self) -> bytes:
        """Receive raw bytes."""
        ...
