import select
import sys
import tty
import termios
import serial
import time
import os

# Initialize serial communication
ser = serial.Serial("/dev/ttyUSB0", 57600, timeout=1)
ser.flush()

original_settings = termios.tcgetattr(sys.stdin)


def get_key(timeout=0.1):
    fd = sys.stdin.fileno()
    try:
        tty.setraw(fd)  # Set the terminal to raw mode
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
            ch = sys.stdin.read(1)  # Read one character
        else:
            ch = None  # No key pressed
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, original_settings)  # Restore terminal settings
    return ch

def send_stop():
    ser.write(b'q\n')
    print("Stopping")


# Function to clear the terminal except for the first line
def clear_terminal_but_first():
    os.system('clear')
    print("Press ESC to exit.")

# Main loop to listen for key presses
try:
    print("Press ESC to exit.")

    while True:
        key = get_key()

        if key == '\x1b':  # ESC key
            ser.write(b'exit\n')
            print("Exiting...")
            break

finally:
    ser.close()
    print("Serial connection closed.")

