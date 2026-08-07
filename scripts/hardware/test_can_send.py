import can

bus = can.Bus(
    interface="slcan",
    channel="COM6",
    bitrate=500000,
)

msg = can.Message(
    arbitration_id=0x7DF,
    data=[0x02, 0x3E, 0x00],
    is_extended_id=False,
)

try:
    print("Enviando Tester Present...")
    bus.send(msg)
    print("✅ Frame enviado com sucesso!")

except can.CanError as exc:
    print(f"❌ Erro ao enviar: {exc}")

finally:
    bus.shutdown()
