"""
Recebe frames CAN da interface USB-CAN.

Uso:
    python scripts/hardware/test_can_receive.py
"""

import can


def main() -> None:
    bus = can.Bus(
        interface="slcan",
        channel="COM6",
        bitrate=500000,
    )

    print("===================================")
    print(" OpenDiag - CAN Receiver")
    print("===================================")
    print("Escutando barramento CAN...")
    print("Pressione Ctrl+C para sair.")
    print("===================================")

    try:
        while True:
            msg = bus.recv(timeout=1.0)

            if msg is not None:
                print(
                    f"ID: {msg.arbitration_id:03X} "
                    f"DLC:{msg.dlc} "
                    f"DATA: {' '.join(f'{b:02X}' for b in msg.data)}"
                )

    except KeyboardInterrupt:
        print("\nEncerrando...")

    finally:
        bus.shutdown()


if __name__ == "__main__":
    main()
