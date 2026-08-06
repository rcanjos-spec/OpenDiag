from enum import IntEnum


class SessionType(IntEnum):
    """UDS diagnostic session types."""

    DEFAULT = 0x01
    PROGRAMMING = 0x02
    EXTENDED = 0x03
