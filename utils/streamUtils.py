import serial

from .settings import SERIAL_PORT, BAUD_RATE

def openSerialConnection():
    # Open serial connection
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Listening on {SERIAL_PORT} at {BAUD_RATE} baud...")

    return ser