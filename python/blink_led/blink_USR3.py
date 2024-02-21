import Adafruit_BBIO.GPIO as GPIO
import time

"""
--------------------------------------------------------------------------
Blink LED
--------------------------------------------------------------------------
License:   
Copyright 2024 - Gloria Ni

Simple function that will for each cycle
  - Turn the USR3 LED on for 0.1 second
  - Turn the USR3 LED off for 0.1 second

Operations:
  - Blinks USR3 LED at a frequency of 5 Hz

Error conditions:
  -None

--------------------------------------------------------------------------

"""

if __name__ == "__main__":
    GPIO.setup("USR%d" % 3, GPIO.OUT)

    while True:

        GPIO.output("USR%d" % 3, GPIO.HIGH)
        time.sleep(0.1)
    
        GPIO.output("USR%d" % 3, GPIO.LOW)
        time.sleep(0.1)