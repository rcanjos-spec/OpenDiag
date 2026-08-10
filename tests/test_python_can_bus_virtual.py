import time

from opendiag.bus.python_can import PythonCANBus
from opendiag.core.can_frame import CANFrame


def test_python_can_bus_virtual_send_and_receive() -> None:
    channel = f"opendiag-test-{time.monotonic_ns()}"

    tx_bus = PythonCANBus(
        interface="virtual",
        channel=channel,
        bitrate=500000,
    )

    rx_bus = PythonCANBus(
        interface="virtual",
        channel=channel,
        bitrate=500000,
    )

    try:
        frame = CANFrame(
            arbitration_id=0x7E0,
            data=b"\x02\x3e\x00",
            timestamp=0.0,
        )

        tx_bus.send(frame)

        received = rx_bus.receive(timeout=1.0)

        assert received is not None
        assert received.arbitration_id == 0x7E0
        assert received.data == b"\x02\x3e\x00"
        assert received.is_extended_id is False

    finally:
        tx_bus.shutdown()
        rx_bus.shutdown()
