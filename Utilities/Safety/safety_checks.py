# Standard Library
import coloredlogs
import drone_exceptions
import logging
import threading
import time

# Ours
from .. import constants as c
from ..two_way_event import TwoWayEvent
from ...Drone.drone import Drone
from ...tools.data_splitter import DataSplitter

class SafetyChecking(threading.Thread):
    """
    This class checks that the drone is behaving as expected, and
    if not, alerts the safety loop on the main thread via setting
    an event.

    Parameters
    ----------
    event: TwoWayEvent
        Set whenever an unsafe condition is found
    drone: Drone
        Interface to the drones information
    enabled: Boolean
        Set to true if the loop should continue to run,
        and false otherwise
    """

    def __init__(self):
        super(SafetyChecking, self).__init__()
        self.setName("SafetyCheckThread")
        self.daemon = True # Means that this thread will abrupty shut down upon main thread exiting
        self.event = TwoWayEvent()
        self.drone = Drone.getDrone()
        self.logger = logging.getLogger(__name__)
        self.enabled = True 

        self.rtg = DataSplitter(['altitude'], use_rtg=True)   

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
            self.rtg.exit()
            self.enabled = False

    def run(self):
        self.started = True
        while self.enabled:
            self.update()
            time.sleep(c.HALF_SEC)

    def get_safety_check_event(self):
        return self.event

    def disable(self):
        self.enabled = False
    
    def enable(self):
        self.enabled = True
