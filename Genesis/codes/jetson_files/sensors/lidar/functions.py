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
#ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)

for pin_pair in left_motor_pins + right_motor_pins: 
    GPIO.setup(pin_pair[0], GPIO.OUT)
    GPIO.setup(pin_pair[1], GPIO.OUT)

def move_forward():
    for pin1, pin2 in left_motor_pins + right_motor_pins:
        GPIO.output(pin1, GPIO.HIGH)
        GPIO.output(pin2, GPIO.LOW)

def move_backward():
    for pin1, pin2 in left_motor_pins + right_motor_pins:
        GPIO.output(pin2, GPIO.HIGH)
        GPIO.output(pin1, GPIO.LOW)

def stop():
    for pin1, pin2 in left_motor_pins + right_motor_pins:
        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.LOW)

def rotate(angle, direction='left', time_constant=0.02):
    rotation_time = angle * time_constant
    
    if direction == 'left':
        for pin1, pin2 in left_motor_pins:
            GPIO.output(pin1, GPIO.LOW)
            GPIO.output(pin2, GPIO.HIGH)
        
        for pin1, pin2 in right_motor_pins:
            GPIO.output(pin1, GPIO.HIGH)
            GPIO.output(pin2, GPIO.LOW)

    elif direction == 'right':
        for pin1, pin2 in left_motor_pins:
            GPIO.output(pin1, GPIO.HIGH)
            GPIO.output(pin2, GPIO.LOW)
        
        for pin1, pin2 in right_motor_pins:
            GPIO.output(pin1, GPIO.LOW)
            GPIO.output(pin2, GPIO.HIGH)

    time.sleep(rotation_time)
    stop()

def receive_data():
    if ser.in_waiting > 0:
        data = ser.readline().decode().strip()
        return data

def mov(direction, t):
    try:
        t = float(t)  # convert t to float in case of decimals
        if direction == 'w':
            move_forward()
            time.sleep(t)
        elif direction == 's':
            move_backward()
            time.sleep(t)
        elif direction == 'a':
            rotate(90, 'left')
        elif direction == 'd':
            rotate(90, 'right')
        elif direction == 'q':
            stop()
            return
        else:
            print("Invalid command!")
    except ValueError:
        print("Error in time conversion.")
    stop()

'''
try:
    print(
    move_backward()
    time.sleep(5)
    stop()
    move_forward()
    time.sleep(5)
    rotate(90, 'right')
    move_forward()
    time.sleep(2)
    rotate(90, 'right')
    move_forward()
    time.sleep(5)
    stop()
finally:
    stop()
    ser.close()
    GPIO.cleanup()
'''
