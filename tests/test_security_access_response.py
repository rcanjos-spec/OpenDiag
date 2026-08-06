from opendiag.uds.responses.security_access import (
    SecurityAccessResponse,
)


def test_create_security_access_response() -> None:
    response = SecurityAccessResponse(
        sid=0x67,
        security_level=0x01,
        data=b"\x12\x34\x56\x78",
    )

    assert response.sid == 0x67
    assert response.security_level == 0x01
    assert response.data == b"\x12\x34\x56\x78"


def test_create_security_access_response_from_bytes() -> None:
    response = SecurityAccessResponse.from_bytes(
        b"\x67\x01\x12\x34\x56\x78",
    )

    assert response.sid == 0x67
    assert response.security_level == 0x01
    assert response.data == b"\x12\x34\x56\x78"
