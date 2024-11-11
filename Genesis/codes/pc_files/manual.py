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

# Store the original terminal settings to restore later
if os.isatty(sys.stdin.fileno()):
        original_settings = termios.tcgetattr(sys.stdin)
else:
    original_settings = None


'''
# Function to get a single keypress without showing on the screen
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
'''
# Function to send stop signal
def send_stop():
    ser.write(b'q\n')
    print("Stopping")


def get_key(timeout=0.1):
    if original_settings is None:  # We're not in a terminal, skip key reading
        return None

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

# Function to clear the terminal except for the first line
def clear_terminal_but_first():
    os.system('clear')
    print("Use keys 'w', 'a', 's', 'd' to move. Press ESC to exit.")

# Main loop to listen for key presses
try:
    print("Use keys 'w', 'a', 's', 'd' to move.")
    print("Press ESC to exit.")
    last_key = None  # Keep track of the last pressed key
    stop_sent = False  # To ensure we only send stop once

    while True:
        key = get_key()

        if key == 'w':
            clear_terminal_but_first()  # Clear terminal except for first line
            ser.write(b'w\n')
            print("Moving Forward")
            last_key = 'w'
            stop_sent = False  # Stop hasn't been sent yet
        elif key == 'a':
            clear_terminal_but_first()
            ser.write(b'a\n')
            print("Turning Left")
            last_key = 'a'
            stop_sent = False
        elif key == 's':
            clear_terminal_but_first()
            ser.write(b's\n')
            print("Moving Backward")
            last_key = 's'
            stop_sent = False
        elif key == 'd':
            clear_terminal_but_first()
            ser.write(b'd\n')
            print("Turning Right")
            last_key = 'd'
            stop_sent = False
        elif key == '\x1b':  # ESC key
            clear_terminal_but_first()
            ser.write(b'exit\n')
            print("Exiting...")
            break
        elif key is None and not stop_sent:
            # No key was pressed in the last check, so stop the rover
            clear_terminal_but_first()
            send_stop()
            stop_sent = True  # Avoid sending multiple stop commands

finally:
    ser.close()
    print("Serial connection closed.")

