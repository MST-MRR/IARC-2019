# Standard Library
import coloredlogs
import constants as c
import drone_exceptions
import logging
import threading
import time

class FailsafeController(threading.Thread):
    """
    This class is a failsafe controller to ensure the copter lands safely in the event of an error.
    """
    def __init__(self, drone):
        super(FailsafeController, self).__init__()
        self.event = threading.Event()
        self.drone = drone 
        self.logger = logging.getLogger(__name__)

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
            self.event.set()
            msg = str(type(e)) + " Error"
            self.logger.critical(msg)

    def run(self):
        self.started = True
        while(not self.event.is_set()):
            self.update()
            time.sleep(c.HALF_SEC)

    def get_failesafe_event(self):
        return self.event