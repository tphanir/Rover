import Jetson.GPIO as GPIO
import time

# Pin Definitions
IN1 = 26  # Example GPIO pin connected to L298N IN1
IN2 = 20

IN3 = 16
IN4 = 19

# Pin Setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Test Output
GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(IN3, GPIO.HIGH)
GPIO.output(IN4, GPIO.LOW)
# Wait and observe motor behavior
time.sleep(5)

# Cleanup
GPIO.cleanup()
