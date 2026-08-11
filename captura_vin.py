import time

import can

LOG_FILE = "captura_vin.txt"

bus = can.Bus(
    interface="slcan",
    channel="COM6",
    bitrate=500000,
)

try:
    print("=== OPEN DIAG - TESTE VIN ===")
    print("Interface: SLCAN COM6")
    print("Bitrate: 500000")
    print()

    msg = can.Message(
        arbitration_id=0x18DB33F1,
        data=[0x02, 0x09, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00],
        is_extended_id=True,
    )

    print("TX ID=0x18DB33F1 EXT=True DLC=8 DATA=02 09 02 00 00 00 00 00")

    bus.send(msg, timeout=1.0)

    print("TX enviado.")
    print("Capturando CAN por 5 segundos...")
    print()

    deadline = time.monotonic() + 5.0

    while time.monotonic() < deadline:
        frame = bus.recv(timeout=0.05)

        if frame is not None:
            print(
                f"RX ID=0x{frame.arbitration_id:08X} "
                f"EXT={frame.is_extended_id} "
                f"DLC={frame.dlc} "
                f"DATA={bytes(frame.data).hex(' ').upper()}"
            )

    print()
    print("=== FIM DA CAPTURA ===")

finally:
    bus.shutdown()
