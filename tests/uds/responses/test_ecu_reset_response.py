from opendiag.uds.reset import ResetType
from opendiag.uds.responses.ecu_reset import ECUResetResponse


def test_create_response() -> None:
    response = ECUResetResponse(
        sid=0x51,
        reset_type=ResetType.SOFT,
    )

    assert response.sid == 0x51
    assert response.reset_type == ResetType.SOFT


def test_from_bytes() -> None:
    response = ECUResetResponse.from_bytes(
        b"\x51\x03",
    )

    assert response.sid == 0x51
    assert response.reset_type == ResetType.SOFT
