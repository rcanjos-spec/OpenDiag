from unittest.mock import Mock

from opendiag.core.can_frame import CANFrame
from opendiag.tools.diagnostic_scanner import DiagnosticScanner


def test_capture_returns_received_frames() -> None:
    frame_1 = CANFrame(
        arbitration_id=0x0F4,
        data=b"\x01\x02",
        timestamp=0.0,
    )

    frame_2 = CANFrame(
        arbitration_id=0x0FB,
        data=b"\x03\x04",
        timestamp=0.01,
    )

    bus = Mock()
    bus.receive.side_effect = [
        frame_1,
        frame_2,
        None,
    ]

    scanner = DiagnosticScanner(
        bus=bus,
    )

    frames = scanner.capture(
        duration=1.0,
    )

    assert frames == [
        frame_1,
        frame_2,
    ]
