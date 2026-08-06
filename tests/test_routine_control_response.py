from opendiag.uds.responses.routine_control import (
    RoutineControlResponse,
)


def test_create_routine_control_response() -> None:
    response = RoutineControlResponse(
        sid=0x71,
        control_type=0x01,
        routine_id=0xFF00,
        data=b"\x12\x34",
    )

    assert response.sid == 0x71
    assert response.control_type == 0x01
    assert response.routine_id == 0xFF00
    assert response.data == b"\x12\x34"


def test_create_routine_control_response_from_bytes() -> None:
    response = RoutineControlResponse.from_bytes(
        b"\x71\x01\xff\x00\x12\x34",
    )

    assert response.sid == 0x71
    assert response.control_type == 0x01
    assert response.routine_id == 0xFF00
    assert response.data == b"\x12\x34"
