import sys
import tty
import termios
import serial
import os
import time
import subprocess

def open_serial():
  ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)
  ser.flush()
  return ser

def close_serial(ser):
  ser.close()

original_settings = termios.tcgetattr(sys.stdin)

def get_key():
    fd = sys.stdin.fileno()
    try:
        tty.setraw(fd)  # Set the terminal to raw mode
        ch = sys.stdin.read(1)  # Read one character
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, original_settings)  # Restore terminal settings
    return ch



def guide():
  print('Commands:')
  print('1 to run manual mode')
  print('2 to run autonomous mode')


try:
    ser = open_serial()
    guide()
    while True:
        key = get_key()

        if key == '1':  # Run the program
            ser.write(b'manual\n')
            print("Manual Mode")
        elif key == '2':
            ser.write(b'auto\n')
            print("Autonomous Mode")

        elif key == '\x1b':  # ESC key
            ser.write(b'exit\n')
            print("Exiting...")
            break

finally:
    ser.close()
    print("Serial connection closed.")

