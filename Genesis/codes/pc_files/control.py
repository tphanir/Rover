import serial
import time

ser = serial.Serial("/dev/ttyUSB1", 57600, timeout=1)
ser.flush()

print('dir:')
print('w - Front')
print('a - Left')
print('s - Back')
print('d - Right')

try:
  while True:
    data = input("Enter: <dir> <time>\n")

    ser.write(data.encode())

finally:
  ser.close()
