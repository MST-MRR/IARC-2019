import abc
import dronekit
from dronekit import VehicleMode
import time
import math
import threading
import sys

from drone_exceptions import AltitudeException, ThrustException, VelocityException, BadArgumentException
import constants as c
import dronekit_wrappers as dkw


# Description:
#    Wraps DroneKit vehicle and sensors.
# Attributes:
#    int id
#    dronekit.Vehicle drone
#    list<Device> devices
class Drone(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.devices = []
        self.taking_off = False
        self.flying = False
        self.connected = False
        self.vehicle = None

    def connect(self, isInSimulator):
        if isInSimulator:
            self.vehicle = dronekit.connect(c.CONNECTION_STRING_SIMULATOR, wait_ready=True)
            print threading.current_thread().name, ": Connecting to the simulated ardupilot"
        else:
            self.vehicle = dronekit.connect(c.CONNECTION_STRING_REAL, wait_ready=True)
            print threading.current_thread().name, ": Connecting to the real-life ardupilot"

        if self.vehicle is not None:
            self.connected = True

    def altitude(self):
        return self.vehicle.rangefinder.distance

    # Attempts to arm the drone. Will time out eventually to prevent 
    # infinite loop.
    def arm(self, timeout = 30):
        start = time.time()
        self.vehicle.mode = VehicleMode(c.GUIDED_MODE)

        print threading.current_thread().name, ": Arming",
        start = time.time()
        while (not self.vehicle.armed) and (time.time() - start < timeout):
            self.vehicle.armed = True
            time.sleep(1)
            print ".",
            sys.stdout.flush()
        print ""
        print threading.current_thread().name, ": Armed"

    def is_connected(self):
        return self.connected

    def is_armed(self):
        return self.vehicle.armed

    def is_taking_off(self):
        return self.taking_off

    def is_flying(self):
        return self.flying

    def takeoff(self, targetAltitude, stop_event):
        self.taking_off = True
        thrust = c.DEFAULT_TAKEOFF_THRUST

        start_time = time.time()
        cutoff_time = 10
        
        while time.time() - start_time < cutoff_time:
            current_altitude = self.altitude()

            if current_altitude >= targetAltitude*0.95: # Trigger just below target alt.
                print "Reached target altitude"
                break
            elif current_altitude >= targetAltitude*0.6:
                thrust = c.SMOOTH_TAKEOFF_THRUST

            dkw.set_attitude(self.vehicle, thrust=thrust)
            time.sleep(1)
        else:
            self.taking_off = False
            print "Could not take off - trying again"
            return

        self.taking_off = False
        self.flying = True

    def land(self):
        while not self.vehicle.mode == VehicleMode(c.LAND_MODE):
            self.vehicle.mode = VehicleMode(c.LAND_MODE)
        while self.vehicle.armed:
            pass

        self.flying = False

    # Should fill devices list with all of the devices a particular drone has
    @abc.abstractmethod
    def loadDevices(self):
        return

    # TODO - This is currently not being used. Make it into a decorator
    def validate_move(self, direction, velocity, duration, distance):
        if velocity > c.VELOCITY_THRESHOLD:
            raise VelocityException('Velocity threshold exceeded')

        altitude = self.vehicle.rangefinder.distance
        if altitude < c.MINIMUM_ALLOWED_ALTITUDE:
            raise AltitudeException('Dangerously low to ground. Movement aborted')

        # TODO - Other checks?

    # Movement methods (basic implementation provided):
    @abc.abstractmethod
    def move(self, direction, distance, stop_event, velocity=c.DEFAULT_VELOCITY):
        if velocity is None:
            velocity = c.DEFAULT_VELOCITY
        # Calculate duration to send velocity command based on distance and velocity
        duration = int(distance / velocity)

        # Multiply unit vector in direction by the velocity
        vector = tuple(velocity * n for n in direction)
        dkw.send_global_velocity(self.vehicle, vector, duration, stop_event)
    
    # TODO - the threading argument here is dummy
    def hover(self, duration, stop_event):
        dkw.send_global_velocity(self.vehicle,(0,0,0), duration, stop_event)