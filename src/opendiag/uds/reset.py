from __future__ import annotations

from enum import IntEnum


class ResetType(IntEnum):
    """UDS ECU Reset types (ISO 14229)."""

    HARD = 0x01
    KEY_OFF_ON = 0x02
    SOFT = 0x03
    ENABLE_RAPID_POWER_SHUTDOWN = 0x04
    DISABLE_RAPID_POWER_SHUTDOWN = 0x05
