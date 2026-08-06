from dataclasses import dataclass

from opendiag.uds.response import PositiveResponse


@dataclass(slots=True, frozen=True, kw_only=True)
class TesterPresentResponse(PositiveResponse):
    """Positive response for UDS Service 0x3E."""

    __test__ = False

    sub_function: int

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
    ) -> TesterPresentResponse:
        return cls(
            sid=data[0],
            sub_function=data[1],
        )
