"""
Testa a abertura da interface USB-CAN.
"""

import can


def main() -> None:
    bus = None

    try:
        bus = can.Bus(
            interface="slcan",
            channel="COM6",
            bitrate=500000,
        )

        print("✅ Interface aberta com sucesso!")

    except can.CanInitializationError as exc:
        print(f"❌ Erro ao abrir a interface: {exc}")

    finally:
        if bus is not None:
            bus.shutdown()


if __name__ == "__main__":
    main()
