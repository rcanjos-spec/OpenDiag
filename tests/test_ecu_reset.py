from opendiag.uds.reset import ResetType
from opendiag.uds.services.ecu_reset import ECUReset


def test_hard_reset() -> None:
    request = ECUReset(
        reset_type=ResetType.HARD_RESET,
    )

    assert request.reset_type == ResetType.HARD_RESET


def test_hard_reset_data() -> None:
    request = ECUReset(
        reset_type=ResetType.HARD_RESET,
    )

    assert request.data == b"\x11\x01"


def test_key_off_on_reset() -> None:
    request = ECUReset(
        reset_type=ResetType.KEY_OFF_ON_RESET,
    )

    assert request.reset_type == ResetType.KEY_OFF_ON_RESET


def test_key_off_on_reset_data() -> None:
    request = ECUReset(
        reset_type=ResetType.KEY_OFF_ON_RESET,
    )

    assert request.data == b"\x11\x02"


def test_soft_reset() -> None:
    request = ECUReset(
        reset_type=ResetType.SOFT_RESET,
    )

    assert request.reset_type == ResetType.SOFT_RESET


def test_soft_reset_data() -> None:
    request = ECUReset(
        reset_type=ResetType.SOFT_RESET,
    )

    assert request.data == b"\x11\x03"
