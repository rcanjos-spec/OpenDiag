from opendiag.uds.services.read_dtc_information import (
    ReadDTCInformation,
)


def test_read_dtc_information_builds_request() -> None:
    request = ReadDTCInformation(
        subfunction=0x02,
        status_mask=0xFF,
    )

    assert request.data == bytes.fromhex("19 02 FF")


def test_read_dtc_information_uses_default_status_mask() -> None:
    request = ReadDTCInformation(
        subfunction=0x02,
    )

    assert request.data == bytes.fromhex("19 02 FF")


def test_read_dtc_information_accepts_status_mask() -> None:
    request = ReadDTCInformation(
        subfunction=0x02,
        status_mask=0x0F,
    )

    assert request.data == bytes.fromhex("19 02 0F")
