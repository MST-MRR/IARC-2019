import RPi.GPIO as GPIO

class Laser:
    def __init__(self, laser_pin):
        #Pin Setup
        self.laser_pin = laser_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.laser_pin, GPIO.OUT) #Sets the given pin as output

    def on(self):
        GPIO.output(self.laser_pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.laser_pin, GPIO.LOW)