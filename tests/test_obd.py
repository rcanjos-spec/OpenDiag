from unittest.mock import Mock

import pytest

from opendiag.core.can_frame import CANFrame
from opendiag.obd import OBDClient, parse_vin
from opendiag.protocols.isotp_transport import ISOTPTransport


def test_parse_vin_from_mode_09_pid_02_response() -> None:
    response = bytes.fromhex(
        "49 02 01 39 42 44 33 35 38 41 43 47 53 59 4E 34 34 35 30 30"
    )

    assert parse_vin(response) == "9BD358ACGSYN44500"


def test_parse_vin_rejects_wrong_service() -> None:
    response = bytes.fromhex(
        "62 F1 90 39 42 44 33 35 38 41 43 47 53 59 4E 34 34 35 30 30"
    )

    with pytest.raises(ValueError, match="Unexpected OBD response"):
        parse_vin(response)


def test_parse_vin_rejects_wrong_pid() -> None:
    response = bytes.fromhex(
        "49 03 01 39 42 44 33 35 38 41 43 47 53 59 4E 34 34 35 30 30"
    )

    with pytest.raises(ValueError, match="Unexpected OBD response"):
        parse_vin(response)


def test_parse_vin_requires_17_characters() -> None:
    response = bytes.fromhex("49 02 01 39 42 44 33 35 38 41")

    with pytest.raises(ValueError, match="VIN must contain 17 characters"):
        parse_vin(response)


def test_obd_client_reads_vin() -> None:
    transport = Mock()

    transport.receive.return_value = bytes.fromhex(
        "49 02 01 39 42 44 33 35 38 41 43 47 53 59 4E 34 34 35 30 30"
    )

    client = OBDClient(transport=transport)

    assert client.read_vin() == "9BD358ACGSYN44500"

    transport.send.assert_called_once_with(
        b"\x09\x02",
    )


def test_obd_client_reads_vin_from_multiframe_response() -> None:
    bus = Mock()

    bus.receive.side_effect = [
        CANFrame(
            arbitration_id=0x18DAF110,
            data=bytes.fromhex("10 14 49 02 01 39 42 44"),
            timestamp=0.0,
            is_extended_id=True,
        ),
        CANFrame(
            arbitration_id=0x18DAF110,
            data=bytes.fromhex("21 33 35 38 41 43 47 53"),
            timestamp=0.1,
            is_extended_id=True,
        ),
        CANFrame(
            arbitration_id=0x18DAF110,
            data=bytes.fromhex("22 59 4E 34 34 35 30 30"),
            timestamp=0.2,
            is_extended_id=True,
        ),
    ]

    transport = ISOTPTransport(
        bus=bus,
    )

    client = OBDClient(
        transport=transport,
    )

    assert client.read_vin() == "9BD358ACGSYN44500"

    assert bus.receive.call_count == 3


def test_obd_client_reads_vin_from_extended_addressed_transport() -> None:
    bus = Mock()

    bus.receive.side_effect = [
        CANFrame(
            arbitration_id=0x18DAF110,
            data=bytes.fromhex("10 14 49 02 01 39 42 44"),
            timestamp=0.0,
            is_extended_id=True,
        ),
        CANFrame(
            arbitration_id=0x18DAF110,
            data=bytes.fromhex("21 33 35 38 41 43 47 53"),
            timestamp=0.1,
            is_extended_id=True,
        ),
        CANFrame(
            arbitration_id=0x18DAF110,
            data=bytes.fromhex("22 59 4E 34 34 35 30 30"),
            timestamp=0.2,
            is_extended_id=True,
        ),
    ]

    transport = ISOTPTransport(
        bus=bus,
        tx_id=0x18DB33F1,
        tx_extended=True,
        rx_id=0x18DAF110,
    )

    client = OBDClient(
        transport=transport,
    )

    assert client.read_vin() == "9BD358ACGSYN44500"

    assert bus.send.call_count == 2

    request_frame = bus.send.call_args_list[0].args[0]
    flow_control_frame = bus.send.call_args_list[1].args[0]

    assert request_frame.arbitration_id == 0x18DB33F1
    assert request_frame.is_extended_id is True
    assert request_frame.data == bytes.fromhex("02 09 02")

    assert flow_control_frame.arbitration_id == 0x18DB33F1
    assert flow_control_frame.is_extended_id is True
    assert flow_control_frame.data == bytes.fromhex("30 00 00")
