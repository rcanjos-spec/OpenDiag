from __future__ import annotations

from enum import IntEnum


class SecurityLevel(IntEnum):
    """UDS Security Access levels (ISO 14229-1)."""

    LEVEL_1_REQUEST_SEED = 0x01
    LEVEL_1_SEND_KEY = 0x02

    LEVEL_2_REQUEST_SEED = 0x03
    LEVEL_2_SEND_KEY = 0x04
