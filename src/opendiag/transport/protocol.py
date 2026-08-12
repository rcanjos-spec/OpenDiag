"""
Transport abstraction.

Defines the interface required by the diagnostic protocol layer
to send and receive raw protocol data without depending on a
specific transport implementation.
"""

from typing import Protocol


class Transport(Protocol):
    """
    Defines the transport contract used by the diagnostic client.

    Concrete implementations may use different communication
    mechanisms, but they must provide the same send and receive
    operations.
    """

    def send(self, data: bytes) -> None:
        """
        Send raw protocol data through the transport.
        """
        ...

    def receive(self) -> bytes:
        """
        Receive raw protocol data from the transport.

        The returned bytes represent the complete response expected
        by the protocol layer.
        """
        ...
