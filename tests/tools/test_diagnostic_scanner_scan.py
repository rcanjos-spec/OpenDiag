from unittest.mock import Mock

from opendiag.core.can_frame import CANFrame
from opendiag.tools.diagnostic_scanner import DiagnosticScanner


def test_scan_counts_frames_by_arbitration_id() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x00",
            timestamp=0.0,
        ),
        CANFrame(
            arbitration_id=0x0FB,
            data=b"\x01",
            timestamp=0.1,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x02",
            timestamp=0.2,
        ),
    ]

    bus = Mock()
    bus.receive.side_effect = frames + [None]

    scanner = DiagnosticScanner(bus)

    result = scanner.scan(
        duration=1.0,
    )

    assert result == {
        0x0F4: 2,
        0x0FB: 1,
    }


def test_scan_stops_when_duration_expires(monkeypatch) -> None:
    times = iter(
        [
            100.0,
            100.4,
            100.8,
            101.0,
        ]
    )

    monkeypatch.setattr(
        "opendiag.tools.diagnostic_scanner.time.monotonic",
        lambda: next(times),
    )

    bus = Mock()
    bus.receive.side_effect = [
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x00",
            timestamp=0.0,
        ),
        CANFrame(
            arbitration_id=0x0FB,
            data=b"\x01",
            timestamp=0.1,
        ),
    ]

    scanner = DiagnosticScanner(bus)

    result = scanner.scan(
        duration=1.0,
    )

    assert result == {
        0x0F4: 1,
        0x0FB: 1,
    }

    assert bus.receive.call_count == 2
