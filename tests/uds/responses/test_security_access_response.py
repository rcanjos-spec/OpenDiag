from opendiag.uds.responses.security_access import (
    SecurityAccessResponse,
)
from opendiag.uds.security import SecurityLevel


def test_create_response() -> None:
    response = SecurityAccessResponse(
        sid=0x67,
        security_level=SecurityLevel.LEVEL_1_REQUEST_SEED,
        security_data=b"\x12\x34\x56\x78",
    )

    assert response.sid == 0x67
    assert response.security_level == SecurityLevel.LEVEL_1_REQUEST_SEED
    assert response.security_data == b"\x12\x34\x56\x78"


def test_from_bytes() -> None:
    response = SecurityAccessResponse.from_bytes(
        b"\x67\x01\x12\x34\x56\x78",
    )

    assert response.sid == 0x67
    assert response.security_level == SecurityLevel.LEVEL_1_REQUEST_SEED
    assert response.security_data == b"\x12\x34\x56\x78"
