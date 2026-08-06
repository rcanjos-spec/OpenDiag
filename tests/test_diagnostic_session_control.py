from opendiag.uds.services.diagnostic_session_control import (
    DiagnosticSessionControl,
)
from opendiag.uds.session import SessionType


def test_default_session() -> None:
    request = DiagnosticSessionControl(
        session_type=SessionType.DEFAULT,
    )

    assert request.session_type == SessionType.DEFAULT


def test_default_session_data() -> None:
    request = DiagnosticSessionControl(
        session_type=SessionType.DEFAULT,
    )

    assert request.data == b"\x10\x01"


def test_programming_session() -> None:
    request = DiagnosticSessionControl(
        session_type=SessionType.PROGRAMMING,
    )

    assert request.session_type == SessionType.PROGRAMMING


def test_programming_session_data() -> None:
    request = DiagnosticSessionControl(
        session_type=SessionType.PROGRAMMING,
    )

    assert request.data == b"\x10\x02"


def test_extended_session() -> None:
    request = DiagnosticSessionControl(
        session_type=SessionType.EXTENDED,
    )

    assert request.session_type == SessionType.EXTENDED


def test_extended_session_data() -> None:
    request = DiagnosticSessionControl(
        session_type=SessionType.EXTENDED,
    )

    assert request.data == b"\x10\x03"


def test_sid() -> None:
    assert DiagnosticSessionControl.SID == 0x10
