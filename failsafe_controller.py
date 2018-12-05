import threading
import time
import coloredlogs, logging
import drone_exceptions
import constants as c

class FailsafeController(threading.Thread):
    """
    This class is a failsafe controller to ensure the copter lands safely in the event of an error.
    """
    def __init__(self, drone):
        super(FailsafeController, self).__init__()
        self.event = threading.Event()
        self.drone = drone 

    def max_velocity_check(self):
        if self.drone.vehicle.airspeed > 0.01:
            raise drone_exceptions.VelocityExceededThreshold()
        
    def max_altitude_check(self):
        if True == False:
            raise drone_exceptions.AltitudeExceededThreshold()

    def negative_velocity_check(self):
        if True == False:
            raise drone_exceptions.AltitudeNegativeException()

    def rangefinder_check(self):
        if True == False:
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
            print("A type of", e, "exception has occured")

    def run(self):
        self.started = True
        while(not self.event.is_set()):
            self.update()
            time.sleep(c.HALF_SEC)

    def get_failesafe_event(self):
        return self.event