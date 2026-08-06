from dataclasses import dataclass

from opendiag.uds.response import PositiveResponse


@dataclass(slots=True, frozen=True, kw_only=True)
class ReadDataByIdentifierResponse(PositiveResponse):
    """Positive response for UDS Service 0x22."""

    did: int
    value: bytes
