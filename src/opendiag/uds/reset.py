from enum import IntEnum


class ResetType(IntEnum):
    """UDS ECU Reset types (ISO 14229)."""

    HARD_RESET = 0x01
    KEY_OFF_ON_RESET = 0x02
    SOFT_RESET = 0x03
    ENABLE_RAPID_POWER_SHUTDOWN = 0x04
    DISABLE_RAPID_POWER_SHUTDOWN = 0x05
