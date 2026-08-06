from opendiag.uds.services.routine_control import (
    RequestRoutineResults,
    StartRoutine,
    StopRoutine,
)


def test_start_routine() -> None:
    request = StartRoutine(
        routine_id=0xFF00,
    )

    assert request.routine_id == 0xFF00


def test_start_routine_data() -> None:
    request = StartRoutine(
        routine_id=0xFF00,
    )

    assert request.data == b"\x31\x01\xff\x00"


def test_start_routine_sid() -> None:
    assert StartRoutine.SID == 0x31


def test_stop_routine() -> None:
    request = StopRoutine(
        routine_id=0xFF00,
    )

    assert request.routine_id == 0xFF00


def test_request_routine_results() -> None:
    request = RequestRoutineResults(
        routine_id=0xFF00,
    )

    assert request.routine_id == 0xFF00


def test_stop_routine_data() -> None:
    request = StopRoutine(
        routine_id=0xFF00,
    )

    assert request.data == b"\x31\x02\xff\x00"


def test_stop_routine_sid() -> None:
    assert StopRoutine.SID == 0x31
