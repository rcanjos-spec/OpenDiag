from opendiag.uds.security import SecurityLevel
from opendiag.uds.services.security_access import SecurityAccess


def test_request_seed() -> None:
    request = SecurityAccess(
        level=SecurityLevel.LEVEL_1_REQUEST_SEED,
    )

    assert request.data == b"\x27\x01"


def test_send_key() -> None:
    request = SecurityAccess(
        level=SecurityLevel.LEVEL_1_SEND_KEY,
        key=b"\x12\x34\x56\x78",
    )

    assert request.data == b"\x27\x02\x12\x34\x56\x78"


def test_sid() -> None:
    assert SecurityAccess.SID == 0x27


def test_service_id_is_first_byte() -> None:
    request = SecurityAccess(
        level=SecurityLevel.LEVEL_1_REQUEST_SEED,
    )

    assert request.data[0] == SecurityAccess.SID


def test_level_is_second_byte() -> None:
    request = SecurityAccess(
        level=SecurityLevel.LEVEL_2_REQUEST_SEED,
    )

    assert request.data[1] == SecurityLevel.LEVEL_2_REQUEST_SEED
