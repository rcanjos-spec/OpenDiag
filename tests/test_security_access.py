from opendiag.uds.services.security_access import RequestSeed, SendKey


def test_request_seed() -> None:
    request = RequestSeed(
        level=1,
    )

    assert request.level == 1


def test_request_seed_data() -> None:
    request = RequestSeed(
        level=1,
    )

    assert request.data == b"\x27\x01"


def test_request_seed_sid() -> None:
    assert RequestSeed.SID == 0x27


def test_send_key() -> None:
    request = SendKey(
        level=2,
        key=b"\x12\x34\x56\x78",
    )

    assert request.level == 2
    assert request.key == b"\x12\x34\x56\x78"
