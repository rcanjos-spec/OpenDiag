"""
UDS request abstractions.

Defines the base representation used by all UDS service requests.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar


@dataclass(slots=True, frozen=True)
class UDSRequest(ABC):
    """
    Base class for all UDS requests.

    Each concrete UDS service defines its own service identifier
    and provides the binary representation of the request.
    """

    # UDS Service Identifier associated with the request.
    SID: ClassVar[int]

    @property
    @abstractmethod
    def data(self) -> bytes:
        """
        Return the binary representation of the request.

        The returned bytes are passed to the transport layer for
        transmission to the diagnostic target.
        """
        raise NotImplementedError
