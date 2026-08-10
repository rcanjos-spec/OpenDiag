from dataclasses import dataclass, field

from opendiag.core.can_frame import CANFrame


@dataclass(slots=True)
class CANTrafficStatistics:
    """Statistics for a CAN arbitration ID."""

    frame_count: int = 0
    dlc: int = 0
    unique_payloads: int = 0
    frequency_hz: float = 0.0
    period_ms: float = 0.0

    _payloads: set[bytes] = field(
        default_factory=set,
        repr=False,
    )
    _payload_list: list[bytes] = field(
        default_factory=list,
        repr=False,
    )

    _first_timestamp: float | None = field(
        default=None,
        repr=False,
    )

    _last_timestamp: float | None = field(
        default=None,
        repr=False,
    )

    @property
    def payloads(self) -> tuple[bytes, ...]:
        """Return unique observed payloads."""

        return tuple(self._payload_list)


class CANTrafficAnalyzer:
    """Analyze captured CAN traffic."""

    def analyze(
        self,
        frames: list[CANFrame],
    ) -> dict[int, CANTrafficStatistics]:
        """Group captured frames by arbitration ID."""

        result: dict[int, CANTrafficStatistics] = {}

        for frame in frames:
            statistics = result.setdefault(
                frame.arbitration_id,
                CANTrafficStatistics(),
            )

            statistics.frame_count += 1
            statistics.dlc = frame.dlc

            if frame.data not in statistics._payloads:
                statistics._payloads.add(frame.data)
                statistics._payload_list.append(frame.data)

            statistics.unique_payloads = len(
                statistics._payloads,
            )

            if statistics._first_timestamp is None:
                statistics._first_timestamp = frame.timestamp

            statistics._last_timestamp = frame.timestamp

            elapsed = statistics._last_timestamp - statistics._first_timestamp

            if elapsed > 0:
                statistics.frequency_hz = (statistics.frame_count - 1) / elapsed

                statistics.period_ms = 1000.0 / statistics.frequency_hz

        return result
