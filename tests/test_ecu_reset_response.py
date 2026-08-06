from opendiag.uds.responses.ecu_reset import ECUResetResponse


def test_create_ecu_reset_response() -> None:
    response = ECUResetResponse(
        sid=0x51,
        reset_type=0x01,
    )

    assert response.sid == 0x51
    assert response.reset_type == 0x01


def test_create_ecu_reset_response_from_bytes() -> None:
    response = ECUResetResponse.from_bytes(
        b"\x51\x01",
    )

    assert response.sid == 0x51
    assert response.reset_type == 0x01
