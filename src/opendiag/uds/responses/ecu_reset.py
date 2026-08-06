from dataclasses import dataclass

from opendiag.uds.response import PositiveResponse


@dataclass(slots=True, frozen=True, kw_only=True)
class ECUResetResponse(PositiveResponse):
    """Positive response for UDS Service 0x11."""

    reset_type: int

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
    ) -> ECUResetResponse:
        return cls(
            sid=data[0],
            reset_type=data[1],
        )
