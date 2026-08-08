from opendiag.uds.reset import ResetType


def test_hard_reset() -> None:
    assert ResetType.HARD == 0x01


def test_key_off_on_reset() -> None:
    assert ResetType.KEY_OFF_ON == 0x02


def test_soft_reset() -> None:
    assert ResetType.SOFT == 0x03


def test_enable_rapid_power_shutdown() -> None:
    assert ResetType.ENABLE_RAPID_POWER_SHUTDOWN == 0x04


def test_disable_rapid_power_shutdown() -> None:
    assert ResetType.DISABLE_RAPID_POWER_SHUTDOWN == 0x05
