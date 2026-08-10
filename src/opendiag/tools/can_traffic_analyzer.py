from dataclasses import dataclass, field
from itertools import pairwise

from opendiag.core.can_frame import CANFrame


@dataclass(slots=True)
class CANTrafficStatistics:
    """Statistics for a CAN arbitration ID."""

    frame_count: int = 0
    dlc: int = 0
    unique_payloads: int = 0
    frequency_hz: float = 0.0
    period_ms: float = 0.0
    byte_unique_values: tuple[int, ...] = ()
    counter_byte_indices: tuple[int, ...] = ()
    counter_analysis: tuple[CANCounterAnalysis, ...] = ()

    _payloads: set[bytes] = field(
        default_factory=set,
        repr=False,
    )
    _payload_list: list[bytes] = field(
        default_factory=list,
        repr=False,
    )

    _byte_values: list[set[int]] = field(
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


@dataclass(frozen=True, slots=True)
class CANCounterAnalysis:
    """Describe a detected CAN counter byte."""

    byte_index: int
    step: int
    rollover: bool


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

            if not statistics._byte_values:
                statistics._byte_values = [set() for _ in range(frame.dlc)]

            for index, value in enumerate(frame.data):
                statistics._byte_values[index].add(value)

            statistics.byte_unique_values = tuple(
                len(values) for values in statistics._byte_values
            )

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

            for statistics in result.values():
                statistics.counter_byte_indices = self._detect_counter_bytes(
                    statistics,
                )
                statistics.counter_analysis = tuple(
                    CANCounterAnalysis(
                        byte_index=index,
                        step=1,
                        rollover=self._has_counter_rollover(
                            statistics,
                            index,
                        ),
                    )
                    for index in statistics.counter_byte_indices
                )

        return result

    @staticmethod
    def _has_counter_rollover(
        statistics: CANTrafficStatistics,
        byte_index: int,
    ) -> bool:
        """Return whether a counter byte wraps from 0xFF to 0x00."""

        values = [
            payload[byte_index]
            for payload in statistics._payload_list
            if len(payload) > byte_index
        ]

        return any(
            previous == 0xFF and current == 0x00
            for previous, current in pairwise(values)
        )

    @staticmethod
    def _detect_counter_bytes(
        statistics: CANTrafficStatistics,
    ) -> tuple[int, ...]:
        """Detect byte positions with sequential +1 behavior."""

        if len(statistics._payload_list) < 2:
            return ()

        counter_indices: list[int] = []

        for index in range(statistics.dlc):
            values = [
                payload[index]
                for payload in statistics._payload_list
                if len(payload) > index
            ]

            if len(values) < 2:
                continue

            if all(
                (current - previous) % 256 == 1
                for previous, current in pairwise(values)
            ):
                counter_indices.append(index)

        return tuple(counter_indices)
