"""
UDS Routine Control response.

Defines the structured representation of the positive response
returned by the Routine Control service.
"""

from dataclasses import dataclass

from opendiag.uds.response import PositiveResponse


@dataclass(slots=True, frozen=True, kw_only=True)
class RoutineControlResponse(PositiveResponse):
    """
    Positive response for UDS Service 0x31.

    Contains the routine control type, the routine identifier, and
    any additional data returned by the diagnostic server.
    """

    # Prevent pytest from treating this response class as a test class.
    __test__ = False

    # Control type returned by the server.
    control_type: int

    # Identifier of the routine being controlled.
    routine_id: int

    # Additional data returned by the routine.
    data: bytes

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
    ) -> RoutineControlResponse:
        """
        Decode a Routine Control positive response.

        Response layout:

            Byte 0: Positive response SID (0x71)
            Byte 1: Routine control type
            Bytes 2-3: Routine identifier
            Remaining bytes: Routine-specific data
        """
        return cls(
            sid=data[0],
            control_type=data[1],
            routine_id=int.from_bytes(
                data[2:4],
                "big",
            ),
            data=data[4:],
        )
