from dataclasses import dataclass

from opendiag.uds.response import PositiveResponse


@dataclass(frozen=True, slots=True)
class DTC:
    """Represents a diagnostic trouble code."""

    code: int
    status: int

    @property
    def active(self) -> bool:
        """Return whether the DTC is active."""
        return bool(self.status & 0x01)

    @property
    def confirmed(self) -> bool:
        """Return whether the DTC is confirmed."""
        return bool(self.status & 0x08)

    @property
    def pending(self) -> bool:
        """Return whether the DTC is pending."""
        return bool(self.status & 0x04)


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadDTCInformationResponse(PositiveResponse):
    """Positive response for UDS Service 0x19."""

    subfunction: int
    status_availability_mask: int
    dtcs: list[DTC]

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
    ) -> ReadDTCInformationResponse:
        if len(data) < 2:
            raise ValueError("Invalid ReadDTCInformation response")

        sid = data[0]
        subfunction = data[1]

        if len(data) == 2:
            return cls(
                sid=sid,
                subfunction=subfunction,
                status_availability_mask=0,
                dtcs=[],
            )

        status_availability_mask = data[2]

        payload = data[3:]

        if len(payload) % 4 != 0:
            raise ValueError("Invalid ReadDTCInformation response")

        dtcs = []

        for offset in range(0, len(payload), 4):
            code = int.from_bytes(
                payload[offset : offset + 3],
                byteorder="big",
            )
            status = payload[offset + 3]

            dtcs.append(
                DTC(
                    code=code,
                    status=status,
                )
            )

        return cls(
            sid=sid,
            subfunction=subfunction,
            status_availability_mask=status_availability_mask,
            dtcs=dtcs,
        )
