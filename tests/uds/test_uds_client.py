from unittest.mock import Mock

from opendiag.uds.client import UDSClient
from opendiag.uds.reset import ResetType
from opendiag.uds.security import SecurityLevel
from opendiag.uds.services.tester_present import TesterPresent


def test_create_client() -> None:
    client = UDSClient(
        transport=object(),
        parser=object(),
    )

    assert client is not None


def test_send_request() -> None:
    transport = Mock()
    parser = Mock()

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    request = TesterPresent()

    client.send(request)

    transport.send.assert_called_once_with(request.data)


def test_send_receives_response() -> None:
    transport = Mock()
    transport.receive.return_value = b"\x7e\x00"

    parser = Mock()

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    client.send(TesterPresent())

    transport.receive.assert_called_once_with()


def test_send_uses_parser() -> None:
    transport = Mock()
    transport.receive.return_value = b"\x7e\x00"

    parser = Mock()

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    client.send(
        TesterPresent(),
    )

    parser.parse.assert_called_once_with(
        b"\x7e\x00",
    )


def test_send_returns_response() -> None:
    transport = Mock()
    transport.receive.return_value = b"\x7e\x00"

    expected = object()

    parser = Mock()
    parser.parse.return_value = expected

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    response = client.send(TesterPresent())

    assert response is expected


def test_ecu_reset() -> None:
    transport = Mock()

    transport.receive.return_value = b"\x51\x03"

    parser = Mock()

    parser.parse.return_value = "OK"

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    response = client.ecu_reset(
        ResetType.SOFT,
    )

    transport.send.assert_called_once_with(
        b"\x11\x03",
    )

    parser.parse.assert_called_once_with(
        b"\x51\x03",
    )

    assert response == "OK"


def test_security_access() -> None:
    transport = Mock()

    transport.receive.return_value = b"\x67\x01\x12\x34\x56\x78"

    parser = Mock()
    parser.parse.return_value = "OK"

    client = UDSClient(
        transport=transport,
        parser=parser,
    )

    response = client.security_access(
        level=SecurityLevel.LEVEL_1_REQUEST_SEED,
    )

    transport.send.assert_called_once_with(
        b"\x27\x01",
    )

    parser.parse.assert_called_once_with(
        b"\x67\x01\x12\x34\x56\x78",
    )

    assert response == "OK"
