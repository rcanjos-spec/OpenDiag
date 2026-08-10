import pytest

from opendiag.core.can_frame import CANFrame
from opendiag.tools.can_traffic_analyzer import CANTrafficAnalyzer


def test_analyze_groups_frames_by_arbitration_id() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x01\x02",
            timestamp=0.00,
        ),
        CANFrame(
            arbitration_id=0x0FB,
            data=b"\x03\x04",
            timestamp=0.01,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x05\x06",
            timestamp=0.02,
        ),
    ]

    analyzer = CANTrafficAnalyzer()

    result = analyzer.analyze(frames)

    assert result[0x0F4].frame_count == 2
    assert result[0x0FB].frame_count == 1


def test_analyze_records_dlc() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x01\x02\x03\x04",
            timestamp=0.00,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x05\x06\x07\x08",
            timestamp=0.01,
        ),
    ]

    analyzer = CANTrafficAnalyzer()

    result = analyzer.analyze(frames)

    assert result[0x0F4].dlc == 4


def test_analyze_records_unique_payloads() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x01\x02",
            timestamp=0.00,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x01\x02",
            timestamp=0.01,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x03\x04",
            timestamp=0.02,
        ),
    ]

    analyzer = CANTrafficAnalyzer()

    result = analyzer.analyze(frames)

    assert result[0x0F4].unique_payloads == 2


def test_analyze_calculates_frequency() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x01",
            timestamp=10.0,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x01",
            timestamp=10.1,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x01",
            timestamp=10.2,
        ),
    ]

    analyzer = CANTrafficAnalyzer()

    result = analyzer.analyze(frames)

    assert result[0x0F4].frequency_hz == pytest.approx(10.0)
