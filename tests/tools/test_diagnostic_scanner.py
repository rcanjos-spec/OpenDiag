from unittest.mock import Mock

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
