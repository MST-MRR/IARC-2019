import abc
import dronekit
from dronekit import VehicleMode
import time
import math
import threading
from sys import stdout

from drone_exceptions import AltitudeException, ThrustException, VelocityException, BadArgumentException
import constants as c
import dronekit_wrappers as dkw

class Drone(object):
    """
    Wraps a DroneKit.vehicle and sensors

    Data Members
    ----------
    vehicle: DroneKit.Vehicle
        Interface to see parameters and send commands
    devices: List of Device (Device not yet implemented)
        Interface to the drone's devices, such as camera
    connected: Boolean
        True if the drone is connected to Ardupilot
    taking_off: Boolean
        True if the drone is in the middle of taking off
    flying: Boolean
        True if the drone is flying but not taking off
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.vehicle = None
        self.devices = []
        self.connected = False
        self.taking_off = False
        self.flying = False


    def connect(self, isInSimulator):
        """
        Attempts to connect to Ardupilot

        Parameters
        ----------
        isInSimulator: Boolean
            True if the program is intended to run in the Gazebo simulator
            and False if the program is being run on the real-life drone

        Precondition:
        ----------
        None

        Postcondition:
        ----------
        Upon a successful connection, self.connected is set to True.
        The drone is now suitable to be armed.

        Returns:
        ----------
        None
        """
        if isInSimulator:
            self.vehicle = dronekit.connect(c.CONNECTION_STRING_SIMULATOR, wait_ready=True, 
                status_printer=None)
            print threading.current_thread().name, ": Connecting to the simulated ardupilot"
        else:
            self.vehicle = dronekit.connect(c.CONNECTION_STRING_REAL, wait_ready=True, 
                status_printer=None)
            print threading.current_thread().name, ": Connecting to the real-life ardupilot"

        if self.vehicle is not None:
            self.connected = True

    def altitude(self):
        """
        Simple wrapper function to retrieve the distance being read by 
        the drone's rangefinder

        Returns:
        ----------
        double
            The distance from the ground
        """
        return self.vehicle.rangefinder.distance

    def altitude_failsafe(self):
        """
        Simple wrapper function to retrieve the distance being read by 
        the drone's barometer

        Returns:
        ----------
        double
            The distance from the ground
        """
        return self.vehicle.location.global_relative_frame.alt

    def arm(self, timeout = 60):
        """
        Attempts to arm the drone for flight

        Parameters
        ----------
        timeout: Integer (optional)
            The duration in seconds that arming should be attempted before
            giving up and returning

        Precondition:
        ----------
        self.connect has been called and succeeded.

        Postcondition:
        ----------
        Upon successful arm, self.vehicle.armed is True, and false otherwise.
        The drone is now suitable to take off.

        Returns:
        ----------
        None
        """
        start = time.time()
        self.vehicle.mode = VehicleMode(c.GUIDED_MODE)

        print threading.current_thread().name, ": Arming",
        start = time.time()
        while (not self.vehicle.armed) and (time.time() - start < timeout):
            self.vehicle.armed = True
            time.sleep(1)
            print ".",
            stdout.flush()
        if not self.vehicle.armed:
            print threading.current_thread().name, ": Failed to arm"
        else:
            print threading.current_thread().name, ": Armed"

    def is_connected(self):
        """
        Getter for self.connected

        Parameters
        ----------
        None

        Returns:
        ----------
        Boolean
            True if the drone is connected to Ardupilot and false otherwise
        """
        return self.connected

    def is_armed(self):
        """
        Getter for self.vehicle.armed

        Parameters
        ----------
        None

        Returns:
        ----------
        Boolean
            True if the drone is armed and false otherwise
        """
        return self.vehicle.armed

    def is_taking_off(self):
        """
        Getter for self.taking_off

        Parameters
        ----------
        None

        Returns:
        ----------
        Boolean
            True if the drone is in the middle of taking off and false otherwise
        """
        return self.taking_off

    def is_flying(self):
        """
        Getter for self.flying

        Parameters
        ----------
        None

        Returns:
        ----------
        Boolean
            True if the drone flying (but not taking off) and false otherwise
        """
        return self.flying

    def takeoff(self, target_altitude, stop_event):
        """
        Attempts to take off (fly from resting state) the drone

        Parameters
        ----------
        target_altitude: Integer 
            The height in meters the drone should be off the ground after
            this function completes
        stop_event: threading.Event
            Set whenever the current thread is being canceled

        Precondition:
        ----------
        The drone is connected and armed.

        Postcondition:
        ----------
        Upon success: the drone is the requested altitude in the air. This function
        will not cause the drone to hover after reaching target altitude! self.flying
        is set to True.

        Returns:
        ----------
        None
        """
        self.taking_off = True
        thrust = c.DEFAULT_TAKEOFF_THRUST

        start_time = time.time()
        cutoff_time = 10
        
        while time.time() - start_time < cutoff_time:
            current_altitude = self.altitude()

            if current_altitude >= target_altitude*0.95: # Trigger just below target alt.
                print "Reached target altitude"
                break
            elif current_altitude >= target_altitude*0.6:
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

    # TODO - This is currently not being used.
    @abc.abstractmethod
    def loadDevices(self):
        """
        Behavior of this function is currently undefined.
        """
        return

    # TODO - This is currently not being used. Make it into a decorator
    def validate_move(self, direction, velocity, duration, distance):
        """
        Behavior of this function is currently undefined.
        """
        if velocity > c.VELOCITY_THRESHOLD:
            raise VelocityException('Velocity threshold exceeded')

        altitude = self.vehicle.rangefinder.distance
        if altitude < c.MINIMUM_ALLOWED_ALTITUDE:
            raise AltitudeException('Dangerously low to ground. Movement aborted')

        # TODO - Other checks?

    @abc.abstractmethod
    def move(self, direction, distance, stop_event, velocity=c.DEFAULT_VELOCITY):
        """
        Moves the drone along a path.

        Parameters
        ----------
        direction: UP, DOWN, LEFT, RIGHT, FORWARD, BACK (as defined in constants.py) 
            The direction the drone should travel in
        distance: Double
            The distance in meters the drone should travel in the given direction
        stop_event: threading.Event()
            Set whenever the current thread is being canceled

        Precondition:
        ----------
        The drone is flying. Should not called from the main thread.

        Postcondition:
        ----------
        The drone has moved in the specified direction by the specified number of meters

        Returns:
        ----------
        None
        """
        if velocity is None:
            velocity = c.DEFAULT_VELOCITY
        # Calculate duration to send velocity command based on distance and velocity
        duration = int(distance / velocity)

        # Multiply unit vector in direction by the velocity
        vector = tuple(velocity * n for n in direction)
        dkw.send_global_velocity(self.vehicle, vector, duration, stop_event)
    
    def hover(self, duration, stop_event):
        """
        Causes the drone to hover in the air.

        Parameters
        ----------
        duration: Integer
            The number of seconds that the drone should hover in place
        stop_event: threading.Event()
            Set whenever the current thread is being canceled

        Precondition:
        ----------
        The drone is flying. Should not called from the main thread.

        Postcondition:
        ----------
        None

        Returns:
        ----------
        None
        """
        dkw.send_global_velocity(self.vehicle,(0,0,0), duration, stop_event)