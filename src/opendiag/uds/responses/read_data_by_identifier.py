from dataclasses import dataclass

from opendiag.uds.response import PositiveResponse


@dataclass(slots=True, frozen=True, kw_only=True)
class ReadDataByIdentifierResponse(PositiveResponse):
    """Positive response for UDS Service 0x22."""

    did: int
    value: bytes

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
    ) -> ReadDataByIdentifierResponse:
        return cls(
            sid=data[0],
            did=int.from_bytes(data[1:3], "big"),
            value=data[3:],
        )
