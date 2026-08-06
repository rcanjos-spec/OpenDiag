from opendiag.uds.response import UDSResponse


def test_create_response() -> None:
    response = UDSResponse(
        sid=0x62,
    )

    assert response.sid == 0x62
