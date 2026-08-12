import pytest

from opendiag.uds.responses.read_dtc_information import (
    ReadDTCInformationResponse,
)


def test_read_dtc_information_response_parses_dtc() -> None:
    response = ReadDTCInformationResponse.from_bytes(
        bytes.fromhex("59 02 CF 01 07 00 0F 01 30 00 40")
    )

    assert response.sid == 0x59
    assert response.subfunction == 0x02
    assert response.status_availability_mask == 0xCF

    assert len(response.dtcs) == 2

    assert response.dtcs[0].code == 0x010700
    assert response.dtcs[0].status == 0x0F

    assert response.dtcs[1].code == 0x013000
    assert response.dtcs[1].status == 0x40


def test_read_dtc_information_response_parses_no_dtcs() -> None:
    response = ReadDTCInformationResponse.from_bytes(bytes.fromhex("59 02"))

    assert response.sid == 0x59
    assert response.subfunction == 0x02
    assert response.dtcs == []


def test_read_dtc_information_response_rejects_invalid_payload() -> None:
    with pytest.raises(
        ValueError,
        match="Invalid ReadDTCInformation response",
    ):
        ReadDTCInformationResponse.from_bytes(bytes.fromhex("59 02 CF 01 07 00"))
