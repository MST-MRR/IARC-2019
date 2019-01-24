"""
This file contains the class for the laser.
"""
from RPi import GPIO

class Laser:
"""
This has two functions to make 
turing the laser on and off easier

Parameters
----------
    laser_pin : int
        Pass the pin number that the laser is plugged into

Attributes
----------
    _laser_pin : int
        The pin number where the laser is attached
"""
    def __init__(self, laser_pin):
        self._laser_pin = laser_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._laser_pin, GPIO.OUT) #Sets the given pin as output

    def on(self):
        """
        This funtion turns on the laser bound to the laser object
        """
        GPIO.output(self._laser_pin, GPIO.HIGH)

    def off(self):
        """
        This funtion turns off the laser bound to the laser object
        """
        GPIO.output(self._laser_pin, GPIO.LOW)