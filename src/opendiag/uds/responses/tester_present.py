"""
UDS Tester Present response.

Defines the structured representation of the positive response
returned by the Tester Present service.
"""

from dataclasses import dataclass

from opendiag.uds.response import PositiveResponse


@dataclass(slots=True, frozen=True, kw_only=True)
class TesterPresentResponse(PositiveResponse):
    """
    Positive response for UDS Service 0x3E.

    Contains the sub-function returned by the diagnostic server.
    """

    # Prevent pytest from treating this response class as a test class.
    __test__ = False

    # Tester Present sub-function returned by the server.
    sub_function: int

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
    ) -> TesterPresentResponse:
        """
        Decode a Tester Present positive response.

        Response layout:

            Byte 0: Positive response SID (0x7E)
            Byte 1: Tester Present sub-function
        """
        return cls(
            sid=data[0],
            sub_function=data[1],
        )
