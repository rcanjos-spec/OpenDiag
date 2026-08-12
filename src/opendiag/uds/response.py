"""
UDS response abstractions.

Defines the base representation for responses received from a
diagnostic target.
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class UDSResponse:
    """
    Base class for UDS responses.

    A response contains the service identifier associated with the
    response and an optional payload containing service-specific data.
    """

    # Service identifier associated with the response.
    sid: int

    # Raw service-specific data carried by the response.
    payload: bytes = b""


@dataclass(slots=True, frozen=True)
class PositiveResponse(UDSResponse):
    """
    Represents a positive UDS response.

    The SID identifies the service that successfully processed the
    request. Service-specific response classes may extend this
    representation with decoded fields.
    """


@dataclass(slots=True, frozen=True, kw_only=True)
class NegativeResponse(UDSResponse):
    """
    Represents a negative UDS response.

    Negative responses identify the original service request and
    provide a response code describing why the request was rejected
    or could not be completed.
    """

    # SID of the original service request.
    original_sid: int

    # UDS negative response code returned by the target.
    response_code: int
