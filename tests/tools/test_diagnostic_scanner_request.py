from unittest.mock import Mock

import pytest

from opendiag.core.can_frame import CANFrame
from opendiag.tools.diagnostic_scanner import DiagnosticScanner
from opendiag.tools.filters import arbitration_id_filter
from opendiag.uds.filters import response_id_filter


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

    received = scanner.request(
        request,
        response_filter=lambda frame: frame.arbitration_id == 0x7E8,
        timeout=3,
    )

    bus.send.assert_called_once_with(request)
    bus.receive.assert_called_once()

    assert received is response


def test_request_times_out() -> None:
    request = CANFrame(
        arbitration_id=0x7DF,
        data=b"\x02\x3e\x00",
        timestamp=0.0,
    )

    bus = Mock()
    bus.receive.return_value = None

    scanner = DiagnosticScanner(bus)

    with pytest.raises(TimeoutError):
        scanner.request(
            request,
            response_filter=arbitration_id_filter(0x7E8),
            timeout=0.02,
        )

    bus.send.assert_called_once_with(request)


def test_request_uses_filter() -> None:
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

    scanner = DiagnosticScanner(bus)

    received = scanner.request(
        request,
        response_filter=response_id_filter(0x7E8),
    )

    assert received is response
