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

    # Start the subprocess without waiting for it to finish
    child_process = subprocess.Popen(
        ['python3', run], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        universal_newlines=True  # Ensures text mode for stdout/stderr
    )

    # Print stdout and stderr in real-time
    while True:
        output = child_process.stdout.readline()
        if output == '' and child_process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    # Capture and print any remaining error messages after the process exits
    stderr = child_process.stderr.read()
    if stderr:
        print(stderr.strip())
    
    
def receive_data(ser):
    if ser.in_waiting > 0:
        data = ser.readline().decode().strip()
        return data


try:
    ser = open_serial()
    while True:
        data = receive_data(ser)
        if data:
            print("Received command:", data)
            run_program(data, ser)
            ser = open_serial()  # Re-open the serial connection after the program run
finally:
    ser.close()
    print("Serial connection closed.")

