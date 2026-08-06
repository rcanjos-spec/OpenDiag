from opendiag.uds.responses.diagnostic_session_control import (
    DiagnosticSessionControlResponse,
)


def test_create_diagnostic_session_control_response() -> None:
    response = DiagnosticSessionControlResponse(
        sid=0x50,
        session_type=0x03,
    )

    assert response.sid == 0x50
    assert response.session_type == 0x03


def test_create_diagnostic_session_control_response_from_bytes() -> None:
    response = DiagnosticSessionControlResponse.from_bytes(
        b"\x50\x03",
    )

    assert response.sid == 0x50
    assert response.session_type == 0x03
