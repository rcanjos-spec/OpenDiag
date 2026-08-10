import time
from unittest.mock import Mock

import pytest

from opendiag.core.can_frame import CANFrame
from opendiag.tools.diagnostic_scanner import DiagnosticScanner


def test_send_frame() -> None:
    bus = Mock()

    scanner = DiagnosticScanner(
        bus=bus,
    )

    frame = CANFrame(
        arbitration_id=0x7DF,
        data=b"\x02\x3e\x00",
        timestamp=0.0,
    )

    scanner.send(frame)

    bus.send.assert_called_once_with(frame)


def test_receive_frame() -> None:
    expected = CANFrame(
        arbitration_id=0x7E8,
        data=b"\x02\x7e\x00",
        timestamp=0.0,
    )

    bus = Mock()
    bus.receive.return_value = expected

    scanner = DiagnosticScanner(
        bus=bus,
    )

    frame = scanner.receive()

    assert frame is expected
    bus.receive.assert_called_once()


def test_receive_frame_with_timeout() -> None:
    expected = CANFrame(
        arbitration_id=0x7E8,
        data=b"\x02\x7e\x00",
        timestamp=0.0,
    )

    bus = Mock()
    bus.receive.return_value = expected

    scanner = DiagnosticScanner(
        bus=bus,
    )

    frame = scanner.receive(timeout=1.5)

    assert frame is expected
    bus.receive.assert_called_once_with(timeout=1.5)


def test_scan_counts_frames_by_arbitration_id() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x100,
            data=b"\x01",
            timestamp=0.0,
        ),
        CANFrame(
            arbitration_id=0x100,
            data=b"\x02",
            timestamp=0.1,
        ),
        CANFrame(
            arbitration_id=0x200,
            data=b"\x03",
            timestamp=0.2,
        ),
        None,
    ]

    bus = Mock()
    bus.receive.side_effect = frames

    scanner = DiagnosticScanner(
        bus=bus,
    )

    counts = scanner.scan(
        duration=1.0,
    )

    assert counts == {
        0x100: 2,
        0x200: 1,
    }


def test_scan_counts_extended_can_id() -> None:
    frame = CANFrame(
        arbitration_id=0x1E360001,
        data=b"\x01\x02",
        timestamp=0.0,
        is_extended_id=True,
    )

    bus = Mock()
    bus.receive.side_effect = [frame, None]

    scanner = DiagnosticScanner(
        bus=bus,
    )

    counts = scanner.scan(
        duration=1.0,
    )

    assert counts == {
        0x1E360001: 1,
    }
    frames = [
        CANFrame(
            arbitration_id=0x100,
            data=b"\x01",
            timestamp=0.0,
        ),
        CANFrame(
            arbitration_id=0x100,
            data=b"\x02",
            timestamp=0.1,
        ),
        CANFrame(
            arbitration_id=0x200,
            data=b"\x03",
            timestamp=0.2,
        ),
        None,
    ]

    bus = Mock()
    bus.receive.side_effect = frames

    scanner = DiagnosticScanner(
        bus=bus,
    )

    counts = scanner.scan(
        duration=1.0,
    )

    assert counts == {
        0x100: 2,
        0x200: 1,
    }


def test_request_returns_matching_response() -> None:
    request_frame = CANFrame(
        arbitration_id=0x7DF,
        data=b"\x02\x10\x01",
        timestamp=0.0,
    )

    response_frame = CANFrame(
        arbitration_id=0x7E8,
        data=b"\x02\x50\x01",
        timestamp=0.1,
    )

    bus = Mock()
    bus.receive.return_value = response_frame

    scanner = DiagnosticScanner(
        bus=bus,
    )

    response = scanner.request(
        request_frame,
        response_filter=lambda frame: frame.arbitration_id == 0x7E8,
    )

    assert response is response_frame
    bus.send.assert_called_once_with(request_frame)
    bus.receive.assert_called_once()


def test_request_timeout_is_in_seconds() -> None:
    request_frame = CANFrame(
        arbitration_id=0x7DF,
        data=b"\x02\x10\x01",
        timestamp=0.0,
    )

    bus = Mock()
    bus.receive.return_value = None

    scanner = DiagnosticScanner(
        bus=bus,
    )

    start = time.monotonic()

    with pytest.raises(TimeoutError):
        scanner.request(
            request_frame,
            response_filter=lambda frame: frame.arbitration_id == 0x7E8,
            timeout=0.02,
        )

    elapsed = time.monotonic() - start

    assert elapsed >= 0.015
    bus.send.assert_called_once_with(request_frame)
    request_frame = CANFrame(
        arbitration_id=0x7DF,
        data=b"\x02\x10\x01",
        timestamp=0.0,
    )

    bus = Mock()
    bus.receive.return_value = None

    scanner = DiagnosticScanner(
        bus=bus,
    )

    with pytest.raises(TimeoutError):
        scanner.request(
            request_frame,
            response_filter=lambda frame: frame.arbitration_id == 0x7E8,
            timeout=0.01,
        )

    bus.send.assert_called_once_with(request_frame)
