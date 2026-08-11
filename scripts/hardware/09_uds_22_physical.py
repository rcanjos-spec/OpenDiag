import time

import can

TX_ID = 0x18DA10F1
RX_ID = 0x18DAF110
FLOW_CONTROL_ID = 0x18DA10F1


bus = can.Bus(
    interface="slcan",
    channel="COM6",
    bitrate=500000,
)

try:
    request = can.Message(
        arbitration_id=TX_ID,
        data=[0x03, 0x22, 0xF1, 0x90, 0, 0, 0, 0],
        is_extended_id=True,
    )

    flow_control = can.Message(
        arbitration_id=FLOW_CONTROL_ID,
        data=[0x30, 0x00, 0x00, 0, 0, 0, 0, 0],
        is_extended_id=True,
    )

    print("## OpenDiag - UDS 0x22 Physical Addressing")
    print()
    print("Interface : COM6")
    print("Bitrate   : 500000")
    print("TX ID     : 18DA10F1")
    print("RX ID     : 18DAF110")
    print("FC ID     : 18DA10F1")
    print()
    print("Solicitando DID F190...")

    bus.send(request, timeout=1.0)

    deadline = time.monotonic() + 2.0
    flow_control_sent = False

    while time.monotonic() < deadline:
        message = bus.recv(timeout=0.05)

        if message is None:
            continue

        data = bytes(message.data)

        print(f"ID=0x{message.arbitration_id:X} DATA={data.hex(' ').upper()}")

        if (
            message.arbitration_id == RX_ID
            and data
            and (data[0] >> 4) == 0x1
            and not flow_control_sent
        ):
            print("First Frame recebido.")
            print("Enviando Flow Control...")

            bus.send(flow_control, timeout=1.0)
            flow_control_sent = True

finally:
    bus.shutdown()
