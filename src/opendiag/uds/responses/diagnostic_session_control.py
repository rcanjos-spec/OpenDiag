"""
UDS Diagnostic Session Control response.

Defines the structured representation of the positive response
returned by the Diagnostic Session Control service.
"""

from dataclasses import dataclass

from opendiag.uds.response import PositiveResponse
from opendiag.uds.session import SessionType


@dataclass(slots=True, frozen=True, kw_only=True)
class DiagnosticSessionControlResponse(PositiveResponse):
    """
    Positive response for Diagnostic Session Control.

    Contains the active diagnostic session and the timing parameters
    specified by the diagnostic server.
    """

    # Diagnostic session activated by the server.
    session_type: SessionType

    # Maximum response time for normal diagnostic requests, in milliseconds.
    p2_server_max: int

    # Maximum response time when the server requires additional time,
    # in units defined by the UDS specification.
    p2_star_server_max: int

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
    ) -> DiagnosticSessionControlResponse:
        """
        Decode a Diagnostic Session Control positive response.

        Response layout:

            Byte 0: Positive response SID (0x50)
            Byte 1: Diagnostic session type
            Bytes 2-3: P2 server maximum time
            Bytes 4-5: P2* server maximum time
        """
        return cls(
            sid=data[0],
            session_type=SessionType(data[1]),
            p2_server_max=int.from_bytes(data[2:4], "big"),
            p2_star_server_max=int.from_bytes(data[4:6], "big"),
        )
