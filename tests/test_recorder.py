from pathlib import Path

from opendiag.core.can_frame import CANFrame
from opendiag.tools.recorder import Recorder


def test_recorder_records_frame(tmp_path: Path) -> None:
    logfile = tmp_path / "capture.log"

    recorder = Recorder(logfile)

    frame = CANFrame(
        arbitration_id=0x7E0,
        data=b"\x02\x10\x03",
        timestamp=0.0,
    )

    recorder.record(frame)

    assert logfile.exists()

    text = logfile.read_text(encoding="utf-8")

    assert "7E0" in text
    assert "02 10 03" in text


def test_record_creates_parent_directories(tmp_path: Path) -> None:
    filename = tmp_path / "logs" / "session" / "capture.log"

    recorder = Recorder(filename)

    frame = CANFrame(
        arbitration_id=0x7E0,
        data=b"\x02\x10\x03",
        timestamp=0.0,
    )

    recorder.record(frame)

    assert filename.exists()

    text = filename.read_text(encoding="utf-8")

    assert "7E0" in text
    assert "02 10 03" in text
