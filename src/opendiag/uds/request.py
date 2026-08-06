from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar


@dataclass(slots=True, frozen=True)
class UDSRequest(ABC):
    """Base class for all UDS requests."""

    SID: ClassVar[int]

    @property
    @abstractmethod
    def data(self) -> bytes:
        """Return the binary representation of the request."""
        raise NotImplementedError
