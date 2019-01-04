# Standard Library
import abc
import coloredlogs
import dronekit
from dronekit import VehicleMode
import logging
import math
import time
import threading

# Ours
from ..Utilities import constants as c
from ..Utilities import dronekit_wrappers as dkw

class DroneBase(object):
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
    """
    __metaclass__ = abc.ABCMeta

    cnt = 0

    def __init__(self):
        self.vehicle = None
        self.devices = []
        self.connected = False
        self.logger = logging.getLogger(__name__)

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
            self.logger.info(threading.current_thread().name + ": Connecting to the simulated ardupilot")
        else:
            self.vehicle = dronekit.connect(c.CONNECTION_STRING_REAL, wait_ready=True, 
                status_printer=None)
            self.logger.info(threading.current_thread().name + ": Connecting to the real-life ardupilot")

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

        self.logger.info(threading.current_thread().name + ": Arming")
        start = time.time()
        while (not self.vehicle.armed) and (time.time() - start < timeout):
            self.vehicle.armed = True
            time.sleep(1)
        if not self.vehicle.armed:
            self.logger.error(threading.current_thread().name + ": Failed to arm")
        else:
            self.logger.info(threading.current_thread().name + ": Armed")

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

    def takeoff(self, target_altitude, stop_event):
        """
        The drone flies from the ground to desired altitude

        Parameters
        ----------
        target_altitude: Integer 
            The height in meters the drone should be off the ground after
            this function completes
        stop_event: threading.Event
            Event which is set when takeoff should be canceled

        Precondition:
        ----------
        The drone is connected and armed.

        Postcondition:
        ----------
        Upon success: the drone is the requested altitude in the air. 

        Returns:
        ----------
        None
        """
        def takeoff_thread(target_altitude, finished, stop_event):
            self.logger.info(threading.current_thread().name + ": Starting takeoff")
            thrust = c.DEFAULT_TAKEOFF_THRUST

            start_time = time.time()
            cutoff_time = 10
            
            while time.time() - start_time < cutoff_time:
                if stop_event.is_set():
                    self.logger.info(threading.current_thread().name + ": Takeoff halting")
                    break

                current_altitude = self.altitude()

                if current_altitude >= target_altitude*0.95: # Trigger just below target alt.
                    break
                elif current_altitude >= target_altitude*0.6:
                    thrust = c.SMOOTH_TAKEOFF_THRUST

                dkw.set_attitude(self.vehicle, thrust=thrust)
                time.sleep(1)
            else:
                self.logger.error("Could not take off!")
            
            self.logger.info(threading.current_thread().name + ": Finished takeoff")
            finished.set()

        finished = threading.Event()
        threading.Thread(target=takeoff_thread, name="TakeoffThread-" + str(DroneBase.cnt), 
            args=(target_altitude, finished, stop_event)).start()
        DroneBase.cnt += 1
        return finished

    def land(self):
        """
        Lands the drone on the ground

        Parameters
        ----------
        None

        Precondition:
        ----------
        The drone is connected and armed.

        Postcondition:
        ----------
        The drone is on the groun (and ideally not smashed into 1000 pieces)
        
        Returns:
        ----------
        None
        """
        def land_thread(finished):
            self.logger.info(threading.current_thread().name + ": Starting land")
            while not self.vehicle.mode == VehicleMode(c.LAND_MODE):
                self.vehicle.mode = VehicleMode(c.LAND_MODE)
            while self.vehicle.armed:
                pass

            self.logger.info(threading.current_thread().name + ": Finished  land")
            finished.set()

        finished = threading.Event()
        threading.Thread(target=land_thread, name="LandThread-" + str(DroneBase.cnt), 
            args=(finished,)).start()
        DroneBase.cnt += 1
        return finished

    def move(self, direction, distance, stop_event, velocity=c.DEFAULT_VELOCITY):
        """
        Moves the drone along a path.

        Parameters
        ----------
        direction: UP, DOWN, LEFT, RIGHT, FORWARD, BACK (as defined in constants.py) 
            The direction the drone should travel in
        distance: Double
            The distance in meters the drone should travel in the given direction
        emergency_land: threading.Event()
            Set when this movement needs to stop

        Precondition:
        ----------
        The drone is already in the air and not moving anywhere else

        Postcondition:
        ----------
        The drone has moved in the specified direction by the specified number of meters

        Returns:
        ----------
        threading.Event
        """

        # Calculate duration to send velocity command based on distance and velocity
        duration = int(distance / velocity)

        # Multiply unit vector in direction by the velocity
        vector = tuple(velocity * n for n in direction)

        # Make the mavlink message
        msg = dkw.get_velocity_message(self.vehicle.message_factory, vector)

        def move_thread(msg, duration, finished, stop_event):
            self.logger.info(threading.current_thread().name + ": Starting move")
            # Send the message once every second
            for _ in range(0, duration):
                self.vehicle.send_mavlink(msg)
                time.sleep(1)
                if stop_event.is_set():
                    self.logger.info(threading.current_thread().name + ": Movement halting")
                    break

            self.logger.info(threading.current_thread().name + ": Finished move")
            finished.set()

        finished = threading.Event()
        threading.Thread(target=move_thread, name="MovementThread-" + str(DroneBase.cnt), 
            args=(msg, duration, finished, stop_event)).start()
        DroneBase.cnt += 1
        return finished
            
    
    def hover(self, duration, stop_event):
        """
        Causes the drone to hover in the air.

        Parameters
        ----------
        duration: Integer
            The number of seconds that the drone should hover in place
        stop_event: threading.Event()
            Set whenever the hover should stop

        Precondition:
        ----------
        The drone is flying.

        Postcondition:
        ----------
        None

        Returns:
        ----------
        None
        """
        # Make the mavlink message
        msg = dkw.get_velocity_message(self.vehicle.message_factory, (0, 0, 0))

        def hover_thread(msg, duration, finished, stop_event):
            self.logger.info(threading.current_thread().name + ": Starting hover")
            # Send the message once every second
            for _ in range(0, duration):
                self.vehicle.send_mavlink(msg)
                time.sleep(1)
                if stop_event.is_set():
                    self.logger.info(threading.current_thread().name + ": Hover halting")
                    break

            self.logger.info(threading.current_thread().name + ": Finished hover")
            finished.set()

        finished = threading.Event()
        threading.Thread(target=hover_thread, name="HoverThread-" + str(DroneBase.cnt), 
            args=(msg, duration, finished, stop_event)).start()
        DroneBase.cnt += 1
        return finished

    @abc.abstractmethod
    def loadDevices(self):
        """
        Behavior of this function is currently undefined.
        """
        pass
