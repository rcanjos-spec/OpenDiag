import time

import can

bus = can.Bus(
    interface="slcan",
    channel="COM6",
    bitrate=500000,
)

try:
    request = can.Message(
        arbitration_id=0x18DB33F1,
        data=[0x02, 0x09, 0x02, 0, 0, 0, 0, 0],
        is_extended_id=True,
    )

    flow_control = can.Message(
        arbitration_id=0x18DA10F1,
        data=[0x30, 0x00, 0x00, 0, 0, 0, 0, 0],
        is_extended_id=True,
    )

    print("TX REQUEST:")
    print("18DB33F1  02 09 02 00 00 00 00 00")

    bus.send(request, timeout=1.0)

    print("Waiting for First Frame...")

    deadline = time.monotonic() + 2.0
    first_frame = None

    while time.monotonic() < deadline:
        frame = bus.recv(timeout=0.05)

        if frame is None:
            continue

        print(f"RX 0x{frame.arbitration_id:08X}: {bytes(frame.data).hex(' ').upper()}")

        if (
            frame.arbitration_id == 0x18DAF110
            and len(frame.data) > 0
            and (frame.data[0] >> 4) == 0x1
        ):
            first_frame = frame
            break

    if first_frame is None:
        print("First Frame NOT received.")

    else:
        print()
        print("First Frame received.")
        print("TX FLOW CONTROL:")
        print("18DA10F1  30 00 00 00 00 00 00 00")

        bus.send(flow_control, timeout=1.0)

        print("Waiting for Consecutive Frames...")

        deadline = time.monotonic() + 2.0

        while time.monotonic() < deadline:
            frame = bus.recv(timeout=0.05)

            if frame is not None:
                print(
                    f"RX 0x{frame.arbitration_id:08X}: "
                    f"{bytes(frame.data).hex(' ').upper()}"
                )

finally:
    bus.shutdown()
