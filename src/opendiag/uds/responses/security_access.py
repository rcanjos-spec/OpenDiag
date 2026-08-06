from dataclasses import dataclass

from opendiag.uds.response import PositiveResponse


@dataclass(slots=True, frozen=True, kw_only=True)
class SecurityAccessResponse(PositiveResponse):
    """Positive response for UDS Service 0x27."""

    __test__ = False

    security_level: int
    data: bytes

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
    ) -> SecurityAccessResponse:
        return cls(
            sid=data[0],
            security_level=data[1],
            data=data[2:],
        )
