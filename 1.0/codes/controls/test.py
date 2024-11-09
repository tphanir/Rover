import Jetson.GPIO as GPIO

# Use BOARD pin numbering
GPIO.setmode(GPIO.BOARD)

# Define the pin you want to check (e.g., pin 12)
pin = 22

# Set the pin as output
GPIO.setup(pin, GPIO.OUT)

# Set the pin output high (1)
GPIO.output(pin, GPIO.HIGH)

# Now read the pin's value
value = GPIO.input(pin)

# Print the value (1 for HIGH, 0 for LOW)
print(f"Pin {pin} is {'HIGH' if value == GPIO.HIGH else 'LOW'}")

# Cleanup
GPIO.cleanup()

