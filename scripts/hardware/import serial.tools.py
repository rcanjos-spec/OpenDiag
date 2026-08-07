import serial.tools.list_ports

for port in serial.tools.list_ports.comports():
    print(f"Device      : {port.device}")
    print(f"Description : {port.description}")
    print(f"HWID        : {port.hwid}")
    print(f"VID         : {port.vid}")
    print(f"PID         : {port.pid}")
    print("-" * 50)
