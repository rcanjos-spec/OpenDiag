from opendiag.uds.responses.diagnostic_session_control import (
    DiagnosticSessionControlResponse,
)
from opendiag.uds.session import SessionType


def test_create_diagnostic_session_control_response() -> None:
    response = DiagnosticSessionControlResponse(
        sid=0x50,
        session_type=SessionType.EXTENDED,
        p2_server_max=50,
        p2_star_server_max=5000,
    )

    assert response.sid == 0x50
    assert response.session_type == SessionType.EXTENDED
    assert response.p2_server_max == 50
    assert response.p2_star_server_max == 5000

    assert response.sid == 0x50
    assert response.session_type == 0x03


def test_create_diagnostic_session_control_response_from_bytes() -> None:
    response = DiagnosticSessionControlResponse.from_bytes(
        b"\x50\x03",
    )

    assert response.sid == 0x50
    assert response.session_type == 0x03


def test_from_bytes() -> None:
    response = DiagnosticSessionControlResponse.from_bytes(
        b"\x50\x03\x00\x32\x13\x88",
    )

    assert response.sid == 0x50
    assert response.session_type == SessionType.EXTENDED
    assert response.p2_server_max == 50
    assert response.p2_star_server_max == 5000
