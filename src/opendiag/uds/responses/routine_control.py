from dataclasses import dataclass

from opendiag.uds.response import PositiveResponse


@dataclass(slots=True, frozen=True, kw_only=True)
class RoutineControlResponse(PositiveResponse):
    """Positive response for UDS Service 0x31."""

    __test__ = False

    control_type: int
    routine_id: int
    data: bytes

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
    ) -> RoutineControlResponse:
        return cls(
            sid=data[0],
            control_type=data[1],
            routine_id=int.from_bytes(
                data[2:4],
                "big",
            ),
            data=data[4:],
        )
