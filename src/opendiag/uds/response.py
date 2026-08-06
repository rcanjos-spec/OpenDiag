from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class UDSResponse:
    """Base class for UDS responses."""

    sid: int
    payload: bytes = b""


@dataclass(slots=True, frozen=True)
class PositiveResponse(UDSResponse):
    """Positive UDS response."""


@dataclass(slots=True, frozen=True, kw_only=True)
class NegativeResponse(UDSResponse):
    """Negative UDS response."""

    original_sid: int
    response_code: int
