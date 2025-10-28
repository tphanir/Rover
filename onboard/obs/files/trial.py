import serial


port = '/dev/ttyUSB0'
baud = 57600

radio = serial.Serial(port, baud, timeout=1)

while True:
    if radio.in_waiting > 0:
        command = radio.readline().decode('utf-8').strip()
        print(command)
