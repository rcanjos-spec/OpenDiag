import pytest

from opendiag.transport.mock import MockTransport


def test_mock_transport_send_receive() -> None:
    transport = MockTransport()

    transport.queue_response(
        b"\x7e\x00",
    )

    transport.send(
        b"\x3e\x00",
    )

    assert transport.last_request == b"\x3e\x00"
    assert transport.receive() == b"\x7e\x00"


def test_mock_transport_multiple_responses() -> None:
    transport = MockTransport()

    transport.queue_response(
        b"\x01",
    )
    transport.queue_response(
        b"\x02",
    )
    transport.queue_response(
        b"\x03",
    )

    assert transport.receive() == b"\x01"
    assert transport.receive() == b"\x02"
    assert transport.receive() == b"\x03"


def test_mock_transport_receive_without_response() -> None:
    transport = MockTransport()

    with pytest.raises(RuntimeError):
        transport.receive()


def test_mock_transport_updates_last_request() -> None:
    transport = MockTransport()

    transport.send(b"\x10\x03")
    assert transport.last_request == b"\x10\x03"

    transport.send(b"\x22\xf1\x90")
    assert transport.last_request == b"\x22\xf1\x90"
