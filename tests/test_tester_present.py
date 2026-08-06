from opendiag.uds.services.tester_present import (
    TesterPresent as TesterPresentRequest,
)


def test_default_tester_present() -> None:
    request = TesterPresentRequest()

    assert request.suppress_response is False


def test_default_data() -> None:
    request = TesterPresentRequest()

    assert request.data == b"\x3e\x00"


def test_suppress_positive_response() -> None:
    request = TesterPresentRequest(
        suppress_response=True,
    )

    assert request.suppress_response is True


def test_suppress_positive_response_data() -> None:
    request = TesterPresentRequest(
        suppress_response=True,
    )

    assert request.data == b"\x3e\x80"


def test_sid() -> None:
    assert TesterPresentRequest.SID == 0x3E
