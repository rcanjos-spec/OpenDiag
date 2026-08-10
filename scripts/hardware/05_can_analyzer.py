from opendiag.bus.python_can import PythonCANBus
from opendiag.tools.can_traffic_analyzer import CANTrafficAnalyzer
from opendiag.tools.diagnostic_scanner import DiagnosticScanner


def main() -> None:
    bus = None

    try:
        bus = PythonCANBus(
            interface="slcan",
            channel="COM6",
            bitrate=500000,
        )

        scanner = DiagnosticScanner(
            bus=bus,
        )

        analyzer = CANTrafficAnalyzer()

        duration = 10.0

        print("=" * 60)
        print(" OpenDiag CAN Traffic Analyzer")
        print("=" * 60)
        print()
        print("Interface :", "COM6")
        print("Bitrate   :", "500000")
        print("Duration  :", f"{duration:.0f} s")
        print()
        print("Capturando tráfego CAN...")
        print()

        frames = scanner.capture(
            duration=duration,
        )

        statistics = analyzer.analyze(
            frames,
        )

        print()
        print(
            f"{'ID':<12}{'Frames':>8}{'DLC':>7}{'Payloads':>10}{'Hz':>10}{'Period':>12}"
        )
        print("-" * 59)

        for arbitration_id, stats in sorted(statistics.items()):
            identifier = f"0x{arbitration_id:08X}"
            print(
                f"{identifier:<12}{stats.frame_count:>8}{stats.dlc:>7}"
                f"{stats.unique_payloads:>10}{stats.frequency_hz:>10.1f}"
                f"{stats.period_ms:>9.1f} ms"
            )

        print()
        print(f"Frames capturados: {len(frames)}")
        print(f"IDs encontrados:   {len(statistics)}")

        for arbitration_id, stats in sorted(statistics.items()):
            print()
            print(f"0x{arbitration_id:08X}")

            for payload in stats.payloads:
                print(f"  {payload.hex(' ').upper()}")

            if stats.counter_analysis:
                print("  Counter analysis:")

                for counter in stats.counter_analysis:
                    end_bit = counter.bit_offset + counter.width - 1

                    print(
                        f"    byte {counter.byte_index} | "
                        f"bits {counter.bit_offset}-{end_bit} | "
                        f"step +{counter.step} | "
                        f"modulus {counter.modulus} | "
                        f"rollover {'YES' if counter.rollover else 'NO'}"
                    )

            if stats.payload_states:
                print("  Payload states:")

                for state_index, state_payloads in enumerate(
                    stats.payload_states,
                    start=1,
                ):
                    print(f"    State {state_index}: {len(state_payloads)} payload(s)")

                    for payload in state_payloads:
                        print(f"      {payload.hex(' ').upper()}")

                    state_analysis = stats.state_counter_analysis[state_index - 1]

                    if state_analysis:
                        print("      Counter analysis:")

                        for counter in state_analysis:
                            end_bit = counter.bit_offset + counter.width - 1

                            print(
                                f"        byte {counter.byte_index} | "
                                f"bits {counter.bit_offset}-{end_bit} | "
                                f"step +{counter.step} | "
                                f"modulus {counter.modulus} | "
                                f"rollover "
                                f"{'YES' if counter.rollover else 'NO'}"
                            )

    finally:
        if bus is not None:
            bus.shutdown()


if __name__ == "__main__":
    main()
