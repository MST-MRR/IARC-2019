# Standard Library
import coloredlogs
import constants as c
import drone_exceptions
import logging
import threading
import time

# Ours
from two_way_event import TwoWayEvent
from ..Drone.drone import Drone

class SafetyChecking(threading.Thread):
    """
    This class checks that the drone is behaving as expected, and
    if not, alerts the user (currently does not do anything about it!)
    """

    def __init__(self):
        super(SafetyChecking, self).__init__()
        self.setName("SafetyCheckThread")
        self.daemon = True
        self.event = TwoWayEvent()
        self.drone = Drone.getDrone()
        self.logger = logging.getLogger(__name__)
        self.enabled = True    

    def max_velocity_check(self):
        if self.drone.vehicle.airspeed > c.VELOCITY_THRESHOLD:
            raise drone_exceptions.VelocityExceededThreshold()
        
    def max_altitude_check(self):
        if self.drone.vehicle.location.global_relative_frame.alt > c.MAXIMUM_ALLOWED_ALTITUDE:
            raise drone_exceptions.AltitudeExceededThreshold()

    def negative_velocity_check(self):
        if self.drone.vehicle.airspeed < 0.0:
            raise drone_exceptions.AltitudeNegativeException()

    def rangefinder_check(self):
        if self.drone.vehicle.rangefinder.distance < c.RANGEFINDER_MIN - c.RANGEFINDER_EPSILON -.5:
            raise drone_exceptions.RangefinderMalfunction()

    def opticalflow_check(self):
        if True == False:
            raise drone_exceptions.OpticalflowMalfunction()

    def update(self):
        try:
            if self.drone.connected:
                self.max_velocity_check()
                self.max_altitude_check()
                self.negative_velocity_check()
                self.rangefinder_check()
                self.opticalflow_check()
        except Exception as e:
            self.event.set_m()
            msg = str(type(e)) + " Error"
            self.logger.critical(msg)
            self.event.wait_a()
            self.enabled = False

    def run(self):
        self.started = True
        while self.enabled:
            if self.enabled:
                self.update()
            time.sleep(c.HALF_SEC)

    def get_safety_check_event(self):
        return self.event

    def disable(self):
        self.enabled = False
    
    def enable(self):
        self.enabled = True