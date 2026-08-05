import sys

import can
import serial

print("=" * 50)
print("OpenDiag Environment Check")
print("=" * 50)

print(f"Python : {sys.version}")
print(f"Python executable : {sys.executable}")
print(f"python-can : {can.__version__}")
print(f"PySerial : {serial.VERSION}")

print("\nEnvironment OK")
