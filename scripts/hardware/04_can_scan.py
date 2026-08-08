from opendiag.bus.python_can import PythonCANBus
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

        duration = 10.0

        print("=" * 40)
        print(" OpenDiag CAN ID Scanner")
        print("=" * 40)
        print()
        print("Interface :", "COM6")
        print("Bitrate   :", "500000")
        print("Duration  :", f"{duration:.0f} s")
        print()
        print("Escaneando CAN...")
        print()

        counts = scanner.scan(
            duration=duration,
        )

        print()
        print("ID       Frames")
        print("-" * 18)

        for arbitration_id, count in sorted(counts.items()):
            print(f"0x{arbitration_id:03X}    {count}")

        print()
        print(f"IDs encontrados: {len(counts)}")

    finally:
        if bus is not None:
            bus.shutdown()


if __name__ == "__main__":
    main()
