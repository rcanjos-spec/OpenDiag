from unittest.mock import Mock

from opendiag.core.can_frame import CANFrame
from opendiag.tools.diagnostic_scanner import DiagnosticScanner


def test_request_sends_and_receives() -> None:
    request = CANFrame(
        arbitration_id=0x7DF,
        data=b"\x02\x3e\x00",
        timestamp=0.0,
    )

    response = CANFrame(
        arbitration_id=0x7E8,
        data=b"\x02\x7e\x00",
        timestamp=0.0,
    )

    bus = Mock()
    bus.receive.return_value = response

    scanner = DiagnosticScanner(
        bus=bus,
    )

    received = scanner.request(request)

    bus.send.assert_called_once_with(request)
    bus.receive.assert_called_once_with()

    assert received is response
