from opendiag.uds.responses.diagnostic_session_control import (
    DiagnosticSessionControlResponse,
)
from opendiag.uds.session import SessionType


def test_from_bytes() -> None:
    response = DiagnosticSessionControlResponse.from_bytes(
        b"\x50\x03\x00\x32\x13\x88",
    )

    assert response.sid == 0x50
    assert response.session_type == SessionType.EXTENDED
    assert response.p2_server_max == 50
    assert response.p2_star_server_max == 5000


def make_response() -> DiagnosticSessionControlResponse:
    return DiagnosticSessionControlResponse(
        sid=0x50,
        session_type=SessionType.EXTENDED,
        p2_server_max=50,
        p2_star_server_max=5000,
    )


def test_sid() -> None:
    response = make_response()

    assert response.sid == 0x50


def test_session_type() -> None:
    response = make_response()

    assert response.session_type == SessionType.EXTENDED


def test_p2_server_max() -> None:
    response = make_response()

    assert response.p2_server_max == 50


def test_p2_star_server_max() -> None:
    response = make_response()

    assert response.p2_star_server_max == 5000
