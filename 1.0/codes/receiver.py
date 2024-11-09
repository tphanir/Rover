import serial
import subprocess
import os


def open_serial():
    return serial.Serial('/dev/ttyUSB1', 57600, timeout=1)

def close_serial(ser):
    ser.close()


def run_program(data, ser):
    if data == 'manual':
        run = 'controls/manual.py'
    elif data == 'auto':
        run = 'lidar/detect.py'
    elif data == 'exit':
        raise SystemExit
    else:
        return 

    close_serial(ser)
    print('Running ' + run)

    child_process = subprocess.Popen(['python3', run], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = child_process.communicate() 
    print(stdout.decode(), stderr.decode())
    
    
def receive_data():
    if ser.in_waiting > 0:
        data = ser.readline().decode().strip()
        return data

try:
    ser = open_serial()
    while True:
        data = receive_data()
        if data:
            print("Received command:", data)
            run_program(data, ser)
            ser = open_serial()
finally:
    ser.close()
    print("Serial connection closed.")

