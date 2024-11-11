#!/usr/bin/env python3

import Jetson.GPIO as GPIO
import time
import serial

right_motor_pins = [
    (11, 8),
    (9, 25),
    (26, 20)
]

left_motor_pins = [
    (23, 22),
    (6, 12),
    (16, 19)
]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ser = serial.Serial('/dev/ttyUSB1', 57600, timeout=1)

# Set up GPIO for motor control
for pin_pair in left_motor_pins + right_motor_pins:
    GPIO.setup(pin_pair[0], GPIO.OUT)
    GPIO.setup(pin_pair[1], GPIO.OUT)

def move_forward():
    print("Moving forward")
    for pin1, pin2 in left_motor_pins + right_motor_pins:
        GPIO.output(pin1, GPIO.HIGH)
        GPIO.output(pin2, GPIO.LOW)

def move_backward():
    print("Moving backward")
    for pin1, pin2 in left_motor_pins + right_motor_pins:
        GPIO.output(pin2, GPIO.HIGH)
        GPIO.output(pin1, GPIO.LOW)

def stop():
    print("Stopping")
    for pin1, pin2 in left_motor_pins + right_motor_pins:
        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.LOW)

def rotate_continuous(direction='left'):
    if direction == 'left':
        print("Rotating left")
        for pin1, pin2 in left_motor_pins:
            GPIO.output(pin1, GPIO.LOW)
            GPIO.output(pin2, GPIO.HIGH)

        for pin1, pin2 in right_motor_pins:
            GPIO.output(pin1, GPIO.HIGH)
            GPIO.output(pin2, GPIO.LOW)

    elif direction == 'right':
        print("Rotating right")
        for pin1, pin2 in left_motor_pins:
            GPIO.output(pin1, GPIO.HIGH)
            GPIO.output(pin2, GPIO.LOW)

        for pin1, pin2 in right_motor_pins:
            GPIO.output(pin1, GPIO.LOW)
            GPIO.output(pin2, GPIO.HIGH)

def receive_data():
    if ser.in_waiting > 0:
        data = ser.readline().decode().strip()
        return data

try:
    while True:
        data = receive_data()
        if data:
            #print("Received:", data)
            # Move based on the received command
            if data == 'w':
                move_forward()
            elif data == 's':
                move_backward()
            elif data == 'a':
                rotate_continuous('left')  # Rotate left as long as 'a' is pressed
            elif data == 'd':
                rotate_continuous('right')  # Rotate right as long as 'd' is pressed
            elif data == 'q':
                stop()  # Stop when no key is pressed
            elif data == 'exit':
                break
finally:
    print('Exiting Manual Mode')
    ser.close()
    GPIO.cleanup()

