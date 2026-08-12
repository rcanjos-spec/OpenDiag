from opendiag.uds.response import NegativeResponse


def test_parse_negative_response() -> None:
    response = NegativeResponse.from_bytes(
        b"\x7f\x22\x31",
    )

    assert response.sid == 0x7F
    assert response.original_sid == 0x22
    assert response.response_code == 0x31
