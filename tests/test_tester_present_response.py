from opendiag.uds.responses.tester_present import (
    TesterPresentResponse,
)


def test_create_tester_present_response() -> None:
    response = TesterPresentResponse(
        sid=0x7E,
        sub_function=0x00,
    )

    assert response.sid == 0x7E
    assert response.sub_function == 0x00


def test_create_tester_present_response_from_bytes() -> None:
    response = TesterPresentResponse.from_bytes(
        b"\x7e\x00",
    )

    assert response.sid == 0x7E
    assert response.sub_function == 0x00
