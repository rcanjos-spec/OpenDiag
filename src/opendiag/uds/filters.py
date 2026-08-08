"""
UDS frame filters.
"""

from __future__ import annotations

from collections.abc import Callable

from opendiag.core.can_frame import CANFrame


def response_id_filter(
    arbitration_id: int,
) -> Callable[[CANFrame], bool]:
    """Create a filter for a UDS response ID."""

    return lambda frame: frame.arbitration_id == arbitration_id
