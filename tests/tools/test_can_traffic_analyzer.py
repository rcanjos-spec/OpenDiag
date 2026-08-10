import pytest

from opendiag.core.can_frame import CANFrame
from opendiag.tools.can_traffic_analyzer import (
    CANCounterAnalysis,
    CANTrafficAnalyzer,
)


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


def test_analyze_records_payloads() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x01\x02",
            timestamp=0.00,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x03\x04",
            timestamp=0.01,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x01\x02",
            timestamp=0.02,
        ),
    ]

    analyzer = CANTrafficAnalyzer()

    result = analyzer.analyze(frames)

    assert result[0x0F4].payloads == (
        b"\x01\x02",
        b"\x03\x04",
    )


def test_analyze_calculates_period() -> None:
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

    assert result[0x0F4].period_ms == pytest.approx(100.0)


def test_analyze_records_byte_activity() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x10\x20\x30\x40",
            timestamp=0.00,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x10\x21\x30\x40",
            timestamp=0.01,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x10\x22\x30\x40",
            timestamp=0.02,
        ),
    ]

    analyzer = CANTrafficAnalyzer()

    result = analyzer.analyze(frames)

    assert result[0x0F4].byte_unique_values == (
        1,
        3,
        1,
        1,
    )


def test_analyze_does_not_detect_non_sequential_byte_as_counter() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x10\x40\xa2",
            timestamp=0.00,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x20\x40\xa2",
            timestamp=0.01,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x30\x40\xa2",
            timestamp=0.02,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x40\x40\xa2",
            timestamp=0.03,
        ),
    ]

    analyzer = CANTrafficAnalyzer()

    result = analyzer.analyze(frames)

    assert result[0x0F4].counter_byte_indices == ()


def test_analyze_detects_counter_rollover() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\xfc\x40\xa2",
            timestamp=0.00,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\xfd\x40\xa2",
            timestamp=0.01,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\xfe\x40\xa2",
            timestamp=0.02,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\xff\x40\xa2",
            timestamp=0.03,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x00\x40\xa2",
            timestamp=0.04,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x01\x40\xa2",
            timestamp=0.05,
        ),
    ]

    analyzer = CANTrafficAnalyzer()

    result = analyzer.analyze(frames)

    assert result[0x0F4].counter_byte_indices == (0,)


def test_analyze_describes_counter_properties() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\xfc\x40\xa2",
            timestamp=0.00,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\xfd\x40\xa2",
            timestamp=0.01,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\xfe\x40\xa2",
            timestamp=0.02,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\xff\x40\xa2",
            timestamp=0.03,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x00\x40\xa2",
            timestamp=0.04,
        ),
    ]

    analyzer = CANTrafficAnalyzer()

    result = analyzer.analyze(frames)

    assert result[0x0F4].counter_analysis == (
        CANCounterAnalysis(
            byte_index=0,
            step=1,
            rollover=True,
        ),
    )


def test_analyze_describes_counter_without_rollover() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x00\x40\xa2",
            timestamp=0.00,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x01\x40\xa2",
            timestamp=0.01,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x02\x40\xa2",
            timestamp=0.02,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x03\x40\xa2",
            timestamp=0.03,
        ),
    ]

    analyzer = CANTrafficAnalyzer()

    result = analyzer.analyze(frames)

    assert result[0x0F4].counter_analysis == (
        CANCounterAnalysis(
            byte_index=0,
            step=1,
            rollover=False,
        ),
    )


def test_analyze_describes_multiple_counter_bytes() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x200,
            data=b"\x00\x10\xff\x05",
            timestamp=0.00,
        ),
        CANFrame(
            arbitration_id=0x200,
            data=b"\x01\x20\xff\x06",
            timestamp=0.01,
        ),
        CANFrame(
            arbitration_id=0x200,
            data=b"\x02\x30\xff\x07",
            timestamp=0.02,
        ),
        CANFrame(
            arbitration_id=0x200,
            data=b"\x03\x40\xff\x08",
            timestamp=0.03,
        ),
    ]

    analyzer = CANTrafficAnalyzer()

    result = analyzer.analyze(frames)

    assert result[0x200].counter_analysis == (
        CANCounterAnalysis(
            byte_index=0,
            step=1,
            rollover=False,
        ),
        CANCounterAnalysis(
            byte_index=3,
            step=1,
            rollover=False,
        ),
    )
