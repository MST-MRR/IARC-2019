import abc
import dronekit
from dronekit import VehicleMode
import time
import math

from drone_exceptions import AltitudeError, ThrustError, VelocityError, BadArgumentError
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

    def connect(self, isInSimulator):
        if isInSimulator:
            self.vehicle = dronekit.connect(c.CONNECTION_STRING_SIMULATOR, wait_ready=True)
            print("--Connecting to the simulated ardupilot--")
        else:
            self.vehicle = dronekit.connect(c.CONNECTION_STRING_REAL, wait_ready=True)
            print("--Connecting to the real-life ardupilot--")

    def altitude(self):
        return self.vehicle.rangefinder.distance

    # Attempts to arm the drone. Will time out eventually to prevent 
    # infinite loop.
    def arm(self, timeout = 30):
        start = time.time()
        self.vehicle.mode = VehicleMode(c.GUIDED)

        start = time.time()
        while (not self.vehicle.armed) and (time.time() - start < timeout):
            self.vehicle.armed = True
            time.sleep(1)
        print("Armed!")

    def takeoff(self, targetAltitude):
        thrust = c.DEFAULT_TAKEOFF_THRUST

        start_time = time.time()
        cutoff_time = 600

        while time.time() - start_time < cutoff_time:
            current_altitude = self.altitude()

            if current_altitude >= targetAltitude*0.95: # Trigger just below target alt.
                print("Reached target altitude")
                break
            elif current_altitude >= targetAltitude*0.6:
                thrust = c.SMOOTH_TAKEOFF_THRUST

            dkw.set_attitude(self.vehicle, thrust=thrust)
            time.sleep(0.2)
        else:
            raise ThrustError("Could not reach thrust")

    def land(self):
        while not self.vehicle.mode == VehicleMode(c.LAND):
            self.vehicle.mode = VehicleMode(c.LAND)
        while self.vehicle.armed:
            pass

    # Should fill devices list with all of the devices a particular drone has
    @abc.abstractmethod
    def loadDevices(self):
        return

    def validate_move(self, direction, velocity, duration, distance):
        if velocity > c.VELOCITY_THRESHOLD:
            raise VelocityError('Velocity threshold exceeded')

        altitude = self.vehicle.rangefinder.distance
        if altitude < c.MINIMUM_ALLOWED_ALTITUDE:
            raise AltitudeError('Dangerously low to ground. Movement aborted')

        # TODO - Other checks?

    # Movement methods (basic implementation provided):
    @abc.abstractmethod
    def move(self, direction, velocity=c.DEFAULT_VELOCITY, duration=None, distance=None):
        self.validate_move(direction, velocity, duration, distance)

        if not(duration or distance):
            raise BadArgumentError("No duration or distance value given.")

        # If distance is set, fly that distance
        if distance:
            duration = int(distance / c.DEFAULT_VELOCITY)

        # Multiply unit vector in direction by the velocity
        # Else, fly at given velocity for given seconds
        vector = tuple(c.DEFAULT_VELOCITY * n for n in direction)

        dkw.send_global_velocity(self.vehicle, vector, duration)
    
    def hover(self, duration):
        dkw.send_global_velocity(self.vehicle, (0,0,0), duration=duration)