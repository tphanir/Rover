import Jetson.GPIO as GPIO
import time

# Pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor configuration with valid PWM pins
motor_pins = {
    "M1": {"IN1": 12, "IN2": 6, "EN": 18},   # Left motor 1 (PWM pin 18)
    "M2": {"IN1": 9, "IN2": 25, "EN": 19},   # Right motor 1 (PWM pin 19)
    "M3": {"IN1": 26, "IN2": 20, "EN": 12},  # Left motor 2 (PWM pin 12)
    "M4": {"IN3": 16, "IN4": 19, "EN": 13},   # Right motor 2 (PWM pin 13)
}

# Initialize all GPIO pins
for motor, pins in motor_pins.items():
    if "IN1" in pins and "IN2" in pins:  # Setup for motors M1, M2, and M3
        GPIO.setup(pins["IN1"], GPIO.OUT)
        GPIO.setup(pins["IN2"], GPIO.OUT)
    if "IN3" in pins and "IN4" in pins:  # Setup for motor M4
        GPIO.setup(pins["IN3"], GPIO.OUT)
        GPIO.setup(pins["IN4"], GPIO.OUT)
    GPIO.setup(pins["EN"], GPIO.OUT)

# PWM setup using valid PWM pins
left_pwm_1 = GPIO.PWM(motor_pins["M1"]["EN"], 100)  # M1 EN pin (PWM pin 18)
right_pwm_1 = GPIO.PWM(motor_pins["M2"]["EN"], 100) # M2 EN pin (PWM pin 19)
left_pwm_2 = GPIO.PWM(motor_pins["M3"]["EN"], 100)  # M3 EN pin (PWM pin 12)
right_pwm_2 = GPIO.PWM(motor_pins["M4"]["EN"], 100) # M4 EN pin (PWM pin 13)

# Start PWM with desired duty cycles
left_pwm_1.start(80)   # 80% throttle for left motors
left_pwm_2.start(80)
right_pwm_1.start(100) # 100% throttle for right motors
right_pwm_2.start(100)

# Move left motors forward
GPIO.output(motor_pins["M1"]["IN1"], GPIO.HIGH)
GPIO.output(motor_pins["M1"]["IN2"], GPIO.LOW)
GPIO.output(motor_pins["M3"]["IN1"], GPIO.HIGH)
GPIO.output(motor_pins["M3"]["IN2"], GPIO.LOW)

# Move right motors forward
GPIO.output(motor_pins["M2"]["IN1"], GPIO.HIGH)
GPIO.output(motor_pins["M2"]["IN2"], GPIO.LOW)
GPIO.output(motor_pins["M4"]["IN3"], GPIO.HIGH)
GPIO.output(motor_pins["M4"]["IN4"], GPIO.LOW)

# Run for a while
time.sleep(5)

# Stop the motors
left_pwm_1.stop()
right_pwm_1.stop()
left_pwm_2.stop()
right_pwm_2.stop()
GPIO.cleanup()

