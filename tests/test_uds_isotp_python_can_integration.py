import threading
import time

from opendiag.bus.python_can import PythonCANBus
from opendiag.protocols.isotp_transport import ISOTPTransport
from opendiag.uds.client import UDSClient
from opendiag.uds.response_parser import UDSResponseParser
from opendiag.uds.response_registry import ResponseRegistry
from opendiag.uds.services.tester_present import TesterPresent


def test_uds_tester_present_over_virtual_can() -> None:
    channel = f"opendiag-uds-{time.monotonic_ns()}"

    tester_bus = PythonCANBus(
        interface="virtual",
        channel=channel,
        bitrate=500000,
    )

    ecu_bus = PythonCANBus(
        interface="virtual",
        channel=channel,
        bitrate=500000,
    )

    tester_transport = ISOTPTransport(
        bus=tester_bus,
        tx_id=0x7E0,
    )

    ecu_transport = ISOTPTransport(
        bus=ecu_bus,
        tx_id=0x7E8,
    )

    received_request: list[bytes] = []

    def ecu() -> None:
        request = ecu_transport.receive()

        if request is not None:
            received_request.append(request)

            if request == b"\x3e\x00":
                ecu_transport.send(
                    b"\x7e\x00",
                )

    thread = threading.Thread(
        target=ecu,
        daemon=True,
    )

    thread.start()

    try:
        parser = UDSResponseParser(
            ResponseRegistry(),
        )

        client = UDSClient(
            transport=tester_transport,
            parser=parser,
        )

        response = client.send(
            TesterPresent(
                suppress_response=False,
            ),
        )

        thread.join(timeout=1.0)

        assert received_request == [
            b"\x3e\x00",
        ]

        assert response.sub_function == 0x00

    finally:
        tester_bus.shutdown()
        ecu_bus.shutdown()
