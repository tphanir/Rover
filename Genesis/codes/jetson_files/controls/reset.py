import Jetson.GPIO as GPIO

try:
    GPIO.setmode(GPIO.BOARD)
    
finally:
    GPIO.cleanup()

