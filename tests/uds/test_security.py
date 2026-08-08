from opendiag.uds.security import SecurityLevel


def test_level_1_request_seed() -> None:
    assert SecurityLevel.LEVEL_1_REQUEST_SEED == 0x01


def test_level_1_send_key() -> None:
    assert SecurityLevel.LEVEL_1_SEND_KEY == 0x02


def test_level_2_request_seed() -> None:
    assert SecurityLevel.LEVEL_2_REQUEST_SEED == 0x03


def test_level_2_send_key() -> None:
    assert SecurityLevel.LEVEL_2_SEND_KEY == 0x04
