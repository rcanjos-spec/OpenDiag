import pytest

from opendiag.core.can_frame import CANFrame
from opendiag.tools.can_traffic_analyzer import (
    CANCounterAnalysis,
    CANIntegrityAnalysis,
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
            bit_offset=0,
            width=8,
            step=1,
            modulus=256,
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
            bit_offset=0,
            width=8,
            step=1,
            modulus=256,
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
            bit_offset=0,
            width=8,
            step=1,
            modulus=256,
            rollover=False,
        ),
        CANCounterAnalysis(
            byte_index=3,
            bit_offset=0,
            width=8,
            step=1,
            modulus=256,
            rollover=False,
        ),
    )


def test_analyze_detects_four_bit_counter() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1c\xd3",
            timestamp=0.00,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1d\xce",
            timestamp=0.01,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1e\xe9",
            timestamp=0.02,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1f\xf4",
            timestamp=0.03,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x10\x4f",
            timestamp=0.04,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x11\x52",
            timestamp=0.05,
        ),
    ]

    analyzer = CANTrafficAnalyzer()

    result = analyzer.analyze(frames)

    assert result[0x0F4].counter_analysis == (
        CANCounterAnalysis(
            byte_index=6,
            bit_offset=0,
            width=4,
            step=1,
            modulus=16,
            rollover=True,
        ),
    )


def test_analyze_describes_four_bit_counter() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1c\xd3",
            timestamp=0.00,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1d\xce",
            timestamp=0.01,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1e\xe9",
            timestamp=0.02,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1f\xf4",
            timestamp=0.03,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x10\x4f",
            timestamp=0.04,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x11\x52",
            timestamp=0.05,
        ),
    ]

    analyzer = CANTrafficAnalyzer()

    result = analyzer.analyze(frames)

    assert result[0x0F4].counter_analysis == (
        CANCounterAnalysis(
            byte_index=6,
            bit_offset=0,
            width=4,
            step=1,
            modulus=16,
            rollover=True,
        ),
    )


def test_analyze_detects_multiple_payload_states() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x20\x7d\x20\x00\x00\x11\x42",
            timestamp=0.00,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x17\x1c",
            timestamp=0.01,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x18\xa7",
            timestamp=0.02,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x19\xba",
            timestamp=0.03,
        ),
    ]

    analyzer = CANTrafficAnalyzer()

    result = analyzer.analyze(frames)

    assert result[0x0F4].payload_states == (
        (b"\x35\x20\x7d\x20\x00\x00\x11\x42",),
        (
            b"\x35\x21\xff\xe0\x00\x00\x17\x1c",
            b"\x35\x21\xff\xe0\x00\x00\x18\xa7",
            b"\x35\x21\xff\xe0\x00\x00\x19\xba",
        ),
    )


def test_analyze_detects_counter_within_payload_state() -> None:
    frames = [
        # Estado transitório — sem contador sequencial.
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x20\x7d\x20\x00\x00\x11\x42",
            timestamp=0.00,
        ),
        # Estado operacional — contador de 4 bits no byte 6.
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1c\xd3",
            timestamp=0.01,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1d\xce",
            timestamp=0.02,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1e\xe9",
            timestamp=0.03,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1f\xf4",
            timestamp=0.04,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x10\x4f",
            timestamp=0.05,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x11\x52",
            timestamp=0.06,
        ),
    ]

    analyzer = CANTrafficAnalyzer()

    result = analyzer.analyze(frames)

    assert result[0x0F4].state_counter_analysis == (
        (),
        (
            CANCounterAnalysis(
                byte_index=6,
                bit_offset=0,
                width=4,
                step=1,
                modulus=16,
                rollover=True,
            ),
        ),
    )

    frames = [
        # Estado transitório — sem contador sequencial.
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x20\x7d\x20\x00\x00\x11\x42",
            timestamp=0.00,
        ),
        # Estado operacional — contador de 4 bits no byte 6.
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1c\xd3",
            timestamp=0.01,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1d\xce",
            timestamp=0.02,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1e\xe9",
            timestamp=0.03,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1f\xf4",
            timestamp=0.04,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x10\x4f",
            timestamp=0.05,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x11\x52",
            timestamp=0.06,
        ),
    ]

    analyzer = CANTrafficAnalyzer()

    result = analyzer.analyze(frames)

    assert result[0x0F4].state_counter_analysis == (
        (),
        (
            CANCounterAnalysis(
                byte_index=6,
                bit_offset=0,
                width=4,
                step=1,
                modulus=16,
                rollover=True,
            ),
        ),
    )


def test_detects_crc8_sae_j1850() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x0F4,
            data=bytes.fromhex("35 21 FF E0 00 00 1C D3"),
            timestamp=0.00,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=bytes.fromhex("35 21 FF E0 00 00 1D CE"),
            timestamp=0.01,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=bytes.fromhex("35 21 FF E0 00 00 1E E9"),
            timestamp=0.02,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=bytes.fromhex("35 21 FF E0 00 00 1F F4"),
            timestamp=0.03,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=bytes.fromhex("35 21 FF E0 00 00 10 4F"),
            timestamp=0.04,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=bytes.fromhex("35 21 FF E0 00 00 11 52"),
            timestamp=0.05,
        ),
    ]

    analyzer = CANTrafficAnalyzer()
    result = analyzer.analyze(frames)

    integrity = result[0x0F4].integrity_analysis

    assert len(integrity) == 1
    assert integrity[0] == CANIntegrityAnalysis(
        byte_index=7,
        algorithm="CRC-8/SAE-J1850",
        protected_start=0,
        protected_end=6,
        polynomial=0x1D,
        init=0xFF,
        xorout=0xFF,
        matches=6,
        total_frames=6,
    )


@pytest.mark.parametrize(
    ("arbitration_id", "payloads"),
    [
        (
            0x0FB,
            [
                "00 FF FF F7 FA 00 01 4C",
                "00 FF FF F7 FA 00 04 25",
                "00 FF FF F7 FA 00 05 38",
                "00 FF FF F7 FA 00 06 1F",
                "00 FF FF F7 FA 00 07 02",
                "00 FF FF F7 FA 00 08 B9",
                "00 FF FF F7 FA 00 09 A4",
                "00 FF FF F7 FA 00 0A 83",
                "00 FF FF F7 FA 00 0B 9E",
                "00 FF FF F7 FA 00 0C CD",
                "00 FF FF F7 FA 00 0D D0",
                "00 FF FF F7 FA 00 0E F7",
                "00 FF FF F7 FA 00 0F EA",
                "00 FF FF F7 FA 00 00 51",
                "00 FF FF F7 FA 00 02 6B",
                "00 FF FF F7 FA 00 03 76",
            ],
        ),
        (
            0x0FC,
            [
                "00 00 9F F0 00 00 01 68",
                "00 00 9F F0 00 00 04 01",
                "00 00 9F F0 00 00 05 1C",
                "00 00 9F F0 00 00 06 3B",
                "00 00 9F F0 00 00 07 26",
                "00 00 9F F0 00 00 08 9D",
                "00 00 9F F0 00 00 09 80",
                "00 00 9F F0 00 00 0A A7",
                "00 00 9F F0 00 00 0B BA",
                "00 00 9F F0 00 00 0C E9",
                "00 00 9F F0 00 00 0D F4",
                "00 00 9F F0 00 00 0E D3",
                "00 00 9F F0 00 00 0F CE",
                "00 00 9F F0 00 00 00 75",
                "00 00 9F F0 00 00 02 4F",
                "00 00 9F F0 00 00 03 52",
            ],
        ),
        (
            0x0FF,
            [
                "08 FF F3 E6 7C C0 01 02",
                "08 FF F3 E6 7C C0 04 6B",
                "08 FF F3 E6 7C C0 05 76",
                "08 FF F3 E6 7C C0 06 51",
                "08 FF F3 E6 7C C0 07 4C",
                "08 FF F3 E6 7C C0 08 F7",
                "08 FF F3 E6 7C C0 09 EA",
                "08 FF F3 E6 7C C0 0A CD",
                "08 FF F3 E6 7C C0 0B D0",
                "08 FF F3 E6 7C C0 0C 83",
                "08 FF F3 E6 7C C0 0D 9E",
                "08 FF F3 E6 7C C0 0E B9",
                "08 FF F3 E6 7C C0 0F A4",
                "08 FF F3 E6 7C C0 00 1F",
                "08 FF F3 E6 7C C0 02 25",
                "08 FF F3 E6 7C C0 03 38",
            ],
        ),
        (
            0x100,
            [
                "BF F9 F3 3E 7C 00 21 CE",
                "BF F9 F3 3E 7C 00 23 F4",
                "BF F9 F3 3E 7C 00 24 A7",
                "BF F9 F3 3E 7C 00 25 BA",
                "BF F9 F3 3E 7C 00 26 9D",
                "BF F9 F3 3E 7C 00 27 80",
                "BF F9 F3 3E 7C 00 28 3B",
                "BF F9 F3 3E 7C 00 29 26",
                "BF F9 F3 3E 7C 00 2A 01",
                "BF F9 F3 3E 7C 00 2B 1C",
                "BF F9 F3 3E 7C 00 2C 4F",
                "BF F9 F3 3E 7C 00 2D 52",
                "BF F9 F3 3E 7C 00 2E 75",
                "BF F9 F3 3E 7C 00 2F 68",
                "BF F9 F3 3E 7C 00 20 D3",
                "BF F9 F3 3E 7C 00 22 E9",
            ],
        ),
        (
            0x1F4,
            [
                "00 00 01 C0 00 00 07 92",
                "00 00 01 C0 00 00 04 B5",
                "00 00 01 C0 00 00 05 A8",
                "00 00 01 C0 00 00 06 8F",
                "00 00 01 C0 00 00 08 29",
                "00 00 01 C0 00 00 09 34",
                "00 00 01 C0 00 00 0A 13",
                "00 00 01 C0 00 00 0B 0E",
                "00 00 01 C0 00 00 0C 5D",
                "00 00 01 C0 00 00 0D 40",
                "00 00 01 C0 00 00 0E 67",
                "00 00 01 C0 00 00 0F 7A",
                "00 00 01 C0 00 00 00 C1",
                "00 00 01 C0 00 00 01 DC",
                "00 00 01 C0 00 00 02 FB",
                "00 00 01 C0 00 00 03 E6",
            ],
        ),
    ],
)
def test_detects_crc8_sae_j1850_for_multiple_ids(
    arbitration_id: int,
    payloads: list[str],
) -> None:
    frames = [
        CANFrame(
            arbitration_id=arbitration_id,
            data=bytes.fromhex(payload),
            timestamp=index * 0.01,
        )
        for index, payload in enumerate(payloads)
    ]

    analyzer = CANTrafficAnalyzer()
    result = analyzer.analyze(frames)

    assert result[arbitration_id].integrity_analysis == (
        CANIntegrityAnalysis(
            byte_index=7,
            algorithm="CRC-8/SAE-J1850",
            protected_start=0,
            protected_end=6,
            polynomial=0x1D,
            init=0xFF,
            xorout=0xFF,
            matches=16,
            total_frames=16,
        ),
    )


def test_analyze_detects_counter_and_crc8_together() -> None:
    frames = [
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1c\xd3",
            timestamp=0.00,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1d\xce",
            timestamp=0.01,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1e\xe9",
            timestamp=0.02,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x1f\xf4",
            timestamp=0.03,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x10\x4f",
            timestamp=0.04,
        ),
        CANFrame(
            arbitration_id=0x0F4,
            data=b"\x35\x21\xff\xe0\x00\x00\x11\x52",
            timestamp=0.05,
        ),
    ]

    result = CANTrafficAnalyzer().analyze(frames)
    statistics = result[0x0F4]

    assert statistics.counter_analysis == (
        CANCounterAnalysis(
            byte_index=6,
            bit_offset=0,
            width=4,
            step=1,
            modulus=16,
            rollover=True,
        ),
    )

    assert statistics.integrity_analysis == (
        CANIntegrityAnalysis(
            byte_index=7,
            algorithm="CRC-8/SAE-J1850",
            protected_start=0,
            protected_end=6,
            polynomial=0x1D,
            init=0xFF,
            xorout=0xFF,
            matches=6,
            total_frames=6,
        ),
    )
