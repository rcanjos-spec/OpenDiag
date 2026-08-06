from pathlib import Path

from opendiag.bus.mock import MockCANBus
from opendiag.core.can_frame import CANFrame
from opendiag.logger import Logger
from opendiag.tools.recorder import Recorder
from opendiag.tools.sniffer import Sniffer


def test_sniffer_records_received_frame(tmp_path: Path) -> None:
    bus = MockCANBus()

    frame = CANFrame(
        arbitration_id=0x7E0,
        data=b"\x02\x10\x03",
        timestamp=0.0,
    )

    bus.send(frame)

    recorder = Recorder(tmp_path / "capture.log")
    logger = Logger()

    sniffer = Sniffer(
        bus=bus,
        logger=logger,
        recorder=recorder,
    )

    received = sniffer.receive()

    assert received == frame

    text = (tmp_path / "capture.log").read_text(encoding="utf-8")

    assert "7E0" in text
    assert "02 10 03" in text
