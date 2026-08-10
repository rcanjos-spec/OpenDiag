from dataclasses import dataclass, field
from itertools import pairwise

from opendiag.core.can_frame import CANFrame


@dataclass(frozen=True, slots=True)
class CANCounterAnalysis:
    """Describe a detected CAN counter field."""

    byte_index: int
    bit_offset: int
    width: int
    step: int
    modulus: int
    rollover: bool


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
    payload_states: tuple[tuple[bytes, ...], ...] = ()
    state_counter_analysis: tuple[
        tuple[CANCounterAnalysis, ...],
        ...,
    ] = ()

    _payloads: set[bytes] = field(
        default_factory=set,
        repr=False,
    )
    _payload_list: list[bytes] = field(
        default_factory=list,
        repr=False,
    )

    _state_payloads: dict[bytes, list[bytes]] = field(
        default_factory=dict,
        repr=False,
    )

    _observed_payloads: list[bytes] = field(
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
            statistics._observed_payloads.append(frame.data)

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

                state_key = frame.data[:6]

                state_payloads = statistics._state_payloads.setdefault(
                    state_key,
                    [],
                )

                if frame.data not in state_payloads:
                    state_payloads.append(frame.data)

            statistics.payload_states = tuple(
                tuple(payloads) for payloads in statistics._state_payloads.values()
            )

            statistics.state_counter_analysis = tuple(
                self._detect_counter_analysis_for_payloads(
                    payloads,
                )
                for payloads in statistics.payload_states
            )

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
                statistics.counter_analysis = self._detect_counter_analysis(
                    statistics,
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
            (previous == 0xFF and current == 0x00)
            or ((previous & 0x0F) == 0x0F and (current & 0x0F) == 0x00)
            for previous, current in pairwise(values)
        )

    @staticmethod
    def _detect_counter_analysis_for_payloads(
        payloads: tuple[bytes, ...],
    ) -> tuple[CANCounterAnalysis, ...]:
        """Detect counters within a single payload state."""

        if len(payloads) < 2:
            return ()

        statistics = CANTrafficStatistics()

        statistics.dlc = max(len(payload) for payload in payloads)

        statistics._payload_list = list(payloads)
        statistics._observed_payloads = list(payloads)

        statistics.counter_byte_indices = CANTrafficAnalyzer._detect_counter_bytes(
            statistics,
        )

        return CANTrafficAnalyzer._detect_counter_analysis(
            statistics,
        )

    @staticmethod
    def _detect_counter_analysis(
        statistics: CANTrafficStatistics,
    ) -> tuple[CANCounterAnalysis, ...]:
        """Describe detected CAN counter fields."""

        analysis: list[CANCounterAnalysis] = []

        for index in statistics.counter_byte_indices:
            values = [
                payload[index]
                for payload in statistics._observed_payloads
                if len(payload) > index
            ]

            if len(values) < 2:
                continue

            full_byte_counter = all(
                (current - previous) % 256 == 1
                for previous, current in pairwise(values)
            )

            nibble_values = [value & 0x0F for value in values]

            nibble_counter = all(
                (current - previous) % 16 == 1
                for previous, current in pairwise(nibble_values)
            )

            if full_byte_counter:
                width = 8
                modulus = 256
            elif nibble_counter:
                width = 4
                modulus = 16
            else:
                continue

            rollover = CANTrafficAnalyzer._has_counter_rollover(
                statistics,
                index,
            )

            analysis.append(
                CANCounterAnalysis(
                    byte_index=index,
                    bit_offset=0,
                    width=width,
                    step=1,
                    modulus=modulus,
                    rollover=rollover,
                )
            )

        return tuple(analysis)

    @staticmethod
    def _detect_counter_bytes(
        statistics: CANTrafficStatistics,
    ) -> tuple[int, ...]:
        """Detect byte positions with sequential +1 behavior."""

        if len(statistics._observed_payloads) < 2:
            return ()

        counter_indices: list[int] = []

        for index in range(statistics.dlc):
            values = [
                payload[index]
                for payload in statistics._observed_payloads
                if len(payload) > index
            ]

            if len(values) < 2:
                continue

            nibble_values = [value & 0x0F for value in values]

            if all(
                (current - previous) % 256 == 1
                for previous, current in pairwise(values)
            ) or all(
                (current - previous) % 16 == 1
                for previous, current in pairwise(nibble_values)
            ):
                counter_indices.append(index)

        return tuple(counter_indices)
