"""
Probe de contador CAN no ID 0x0F4.
Captura todos os frames recebidos e mostra os bytes 6 e 7.
"""

import time

import can


def main() -> None:
    bus = None

    try:
        bus = can.Bus(
            interface="slcan",
            channel="COM6",
            bitrate=500000,
        )

        print("=" * 60)
        print(" OpenDiag CAN Counter Probe")
        print("=" * 60)
        print()
        print("Interface :", "COM6")
        print("Bitrate   :", "500000")
        print("Filtro    :", "0x0F4")
        print("Duration  :", "5 s")
        print()
        print("Capturando...")
        print()
        print(f"{'Timestamp':<16}{'ID':<10}{'B6':>4}{'B7':>4}")
        print("-" * 38)

        bus.set_filters([{"can_id": 0x0F4, "can_mask": 0x7FF}])

        start = time.monotonic()
        count = 0

        while time.monotonic() - start < 5.0:
            message = bus.recv(timeout=0.5)

            if message is None:
                continue
            if len(message.data) < 8:
                continue

            count += 1

            print(
                f"{message.timestamp:<16.6f}"
                f"0x{message.arbitration_id:03X}"
                f"{message.data[6]:>4X}"
                f"{message.data[7]:>4X}"
            )

        print()
        print(f"Frames capturados: {count}")

    finally:
        if bus is not None:
            bus.shutdown()


if __name__ == "__main__":
    main()
