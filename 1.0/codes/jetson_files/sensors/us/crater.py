import time
import Jetson.GPIO as GPIO

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for TRIG and ECHO
TRIG = 19  # GPIO pin for Trigger
ECHO = 16  # GPIO pin for Echo

# Set up the GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Crater detection threshold (distance difference in cm that indicates a crater)
CRATER_THRESHOLD = 10  # Adjust this value based on tests

# Function to get distance from ultrasonic sensor
def get_distance():
    # Ensure the trigger pin is LOW
    GPIO.output(TRIG, False)
    time.sleep(0.1)  # Shorter settle time for faster scanning

    # Send a 10us pulse to trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(TRIG, False)

    # Record the start time
    start_time = time.time()
    stop_time = time.time()

    # Wait for the echo to start
    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    # Wait for the echo to stop
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    # Calculate the time difference
    time_elapsed = stop_time - start_time

    # Distance is time elapsed multiplied by the speed of sound (34300 cm/s)
    distance = (time_elapsed * 34300) / 2  # Divide by 2 for the round trip

    return distance

# Crater detection logic
def detect_crater(previous_distance, current_distance):
    distance_diff = previous_distance - current_distance

    # Check if the drop in distance exceeds the crater threshold
    if distance_diff > CRATER_THRESHOLD:
        return True
    return False


try:
    previous_distance = get_distance()  # Initial distance
    while True:
        current_distance = get_distance()
        print(f"Current Distance: {current_distance:.2f} cm")

        if detect_crater(previous_distance, current_distance):
            print("Crater detected!")
        else:
            print("No crater detected")

        previous_distance = current_distance  # Update previous distance
        time.sleep(1)  # Adjust this delay based on your robot's speed and sensor rate

finally:
    
    GPIO.cleanup()  # Clean up GPIO settings

