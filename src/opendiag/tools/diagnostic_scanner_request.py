from unittest.mock import Mock

from opendiag.core.can_frame import CANFrame
from opendiag.tools.diagnostic_scanner import DiagnosticScanner


def test_request_waits_for_expected_response() -> None:
    request = CANFrame(
        arbitration_id=0x7DF,
        data=b"\x02\x3e\x00",
        timestamp=0.0,
    )

    ignored = CANFrame(
        arbitration_id=0x0FB,
        data=b"\x00",
        timestamp=0.0,
    )

    expected = CANFrame(
        arbitration_id=0x7E8,
        data=b"\x02\x7e\x00",
        timestamp=0.0,
    )

    bus = Mock()
    bus.receive.side_effect = [
        ignored,
        expected,
    ]

    scanner = DiagnosticScanner(bus)

    response = scanner.request(
        request,
        response_id=0x7E8,
    )

    assert response is expected
    assert bus.receive.call_count == 2
