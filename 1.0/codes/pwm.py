import Jetson.GPIO as GPIO
import time

# Pin definitions for Left Motors (Motor Driver 1)
ENA_LEFT = 32  # GPIO pin for EN A (left motors)
IN1_LEFT = 33  # GPIO pin for IN1 (left motors)
IN2_LEFT = 35  # GPIO pin for IN2 (left motors)

# Pin definitions for Right Motors (Motor Driver 2)
ENB_RIGHT = 36  # GPIO pin for EN B (right motors)
IN3_RIGHT = 37  # GPIO pin for IN3 (right motors)
IN4_RIGHT = 38  # GPIO pin for IN4 (right motors)

# Pin definitions for Middle Motors (Motor Driver 3)
ENA_MIDDLE = 40  # GPIO pin for EN A (middle motors)
IN1_MIDDLE = 31  # GPIO pin for IN1 (middle motors)
IN2_MIDDLE = 29  # GPIO pin for IN2 (middle motors)

# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ENA_LEFT, GPIO.OUT)
GPIO.setup(IN1_LEFT, GPIO.OUT)
GPIO.setup(IN2_LEFT, GPIO.OUT)

GPIO.setup(ENB_RIGHT, GPIO.OUT)
GPIO.setup(IN3_RIGHT, GPIO.OUT)
GPIO.setup(IN4_RIGHT, GPIO.OUT)

GPIO.setup(ENA_MIDDLE, GPIO.OUT)
GPIO.setup(IN1_MIDDLE, GPIO.OUT)
GPIO.setup(IN2_MIDDLE, GPIO.OUT)

# PWM setup for all motors
pwm_left = GPIO.PWM(ENA_LEFT, 1000)  # Left motors PWM at 1kHz
pwm_right = GPIO.PWM(ENB_RIGHT, 1000)  # Right motors PWM at 1kHz
pwm_middle = GPIO.PWM(ENA_MIDDLE, 1000)  # Middle motors PWM at 1kHz

# Start with 0% duty cycle (motors off)
pwm_left.start(0)
pwm_right.start(0)
pwm_middle.start(0)

def set_motor_speeds(speed_left, speed_right, speed_middle):
    # Ensure the speed is within 0-100% range
    speed_left = min(max(speed_left, 0), 100)
    speed_right = min(max(speed_right, 0), 100)
    speed_middle = min(max(speed_middle, 0), 100)
    
    pwm_left.ChangeDutyCycle(speed_left)
    pwm_right.ChangeDutyCycle(speed_right)
    pwm_middle.ChangeDutyCycle(speed_middle)

def move_forward(speed_left, speed_right, speed_middle):
    # Set left motors to move forward
    GPIO.output(IN1_LEFT, GPIO.HIGH)
    GPIO.output(IN2_LEFT, GPIO.LOW)
    
    # Set right motors to move forward
    GPIO.output(IN3_RIGHT, GPIO.HIGH)
    GPIO.output(IN4_RIGHT, GPIO.LOW)
    
    # Set middle motors to move forward
    GPIO.output(IN1_MIDDLE, GPIO.HIGH)
    GPIO.output(IN2_MIDDLE, GPIO.LOW)
    
    set_motor_speeds(speed_left, speed_right, speed_middle)

def stop_motors():
    # Stop left motors
    GPIO.output(IN1_LEFT, GPIO.LOW)
    GPIO.output(IN2_LEFT, GPIO.LOW)
    
    # Stop right motors
    GPIO.output(IN3_RIGHT, GPIO.LOW)
    GPIO.output(IN4_RIGHT, GPIO.LOW)
    
    # Stop middle motors
    GPIO.output(IN1_MIDDLE, GPIO.LOW)
    GPIO.output(IN2_MIDDLE, GPIO.LOW)
    
    pwm_left.ChangeDutyCycle(0)
    pwm_right.ChangeDutyCycle(0)
    pwm_middle.ChangeDutyCycle(0)

try:
    while True:
        # Example: Moving forward with lane correction
        move_forward(70, 100, 80)  # Left motors at 70%, right motors at 100%, middle motors at 80%
        time.sleep(5)  # Move forward for 5 seconds
        
        stop_motors()  # Stop the rover
        time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    pwm_left.stop()
    pwm_right.stop()
    pwm_middle.stop()
    GPIO.cleanup()
