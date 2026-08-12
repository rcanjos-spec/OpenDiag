"""
UDS Read Data By Identifier response.

Defines the structured representation of responses returned by
the Read Data By Identifier service.
"""

from dataclasses import dataclass

from opendiag.uds.response import PositiveResponse


@dataclass(slots=True, frozen=True, kw_only=True)
class ReadDataByIdentifierResponse(PositiveResponse):
    """
    Positive response for UDS Service 0x22.

    Contains the Data Identifier (DID) requested by the diagnostic
    client and the raw data associated with that identifier.
    """

    # Data Identifier returned by the diagnostic target.
    did: int

    # Raw value associated with the requested DID.
    value: bytes

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
    ) -> ReadDataByIdentifierResponse:
        """
        Decode a raw Read Data By Identifier response.

        The first byte contains the positive response SID, the next
        two bytes contain the DID, and all remaining bytes contain
        the value associated with that DID.
        """
        if len(data) < 3:
            raise ValueError("Invalid ReadDataByIdentifier response")

        return cls(
            sid=data[0],
            did=int.from_bytes(data[1:3], "big"),
            value=data[3:],
        )
