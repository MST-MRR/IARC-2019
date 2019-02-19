import abc

from simple_pid import PID
from dronekit import VehicleMode

from flight import constants as c
from flight import flightconfig as f
from flight.drone.exceptions import EmergencyLandException

KP = 1
KI = 0
KD = 0

class TaskBase():
    """A task the the drone can perform.

    Responsible for implementing the core logic of the various actions that a
    drone can take (ex. Movement, Follow, Heal, Decode). Must implement
    perform().

    Attributes
    ----------
    _drone: dronekit.vehicle
        An interface to the drone.
    _done: bool
        The status of the task.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, drone):
        self._drone = drone
        self._done = False

    @abc.abstractmethod
    def perform(self):
        """Do one iteration of the logic for this task.

        Returns
        --------
        bool
            True if the task is done with its goal, and false otherwise.
        """
        pass

    @property
    def done(self):
        return self._done


class Exit(TaskBase):
    """A task that terminates control of the drone."""

    def __init__(self, drone):
        """Initialize a task for terminating control.

        Parameters
        ----------
        drone : dronekit.Vehicle
            The drone being controlled.
        """
        super(Exit, self).__init__(drone)

    def perform(self):
        # If exit task was called while still in flight, then land.
        if self._drone.armed:
            raise EmergencyLandException

        # Since this is just a flag task, return immediately
        return True


class Hover(TaskBase):
    """A task that makes drone hover for a period of time.

    Attributes
    ----------
    _duration : float
        How long to hover for in seconds.
    _pid_alt : simple_pid.PID
        A PID controller used for altitude.
    _count : int
        An internval variable for keeping track of state.
    """

    def __init__(self, drone, altitude, duration):
        """Initialize a task for hovering.

        Parameters
        ----------
        drone : dronekit.Vehicle
            The drone being controlled.
        altitude : float
            Target altitude to maintain during hover.
        duration : float
            How many seconds to hover for.
        """
        super(Hover, self).__init__(drone)
        self._duration = duration
        self._pid_alt = PID(KP, KI, KP, setpoint=altitude)
        self._count = duration * (1.0/c.DELAY_INTERVAL)

    def perform(self):
        # Get control value
        zv = -self._pid_alt(self._drone.rangefinder.distance)
        # Send 0 velocities to drone (excepting altitude correction)
        self._drone.send_velocity(0, 0, zv)
        self._count -= 1

        return self._count <= 0


class Land(TaskBase):
    """A task that makes the drone land.

    Attributes
    ----------
    _land_mode : dronekit.VehicleMode
        A reference to dronekit's land mode object
    """

    def __init__(self, drone):
        """Initialize a task for landing.

        Parameters
        ----------
        drone : dronekit.Vehicle
            The drone being controlled.
        """
        super(Land, self).__init__(drone)
        self._land_mode = VehicleMode(c.Modes.LAND.value)

    def perform(self):
        if not self._drone.mode == self._land_mode:
            self._drone.mode = self._land_mode
            return False

        return not self._drone.armed


class LinearMovement(TaskBase):
    """A task that moves the drone along an axis."""

    def __init__(self, drone, direction, duration):
        """Initialize a task for moving along an axis.

        Parameters
        ----------
        drone : dronekit.Vehicle
            The drone being controlled.
        direction : Directions.{LEFT, RIGHT, FORWARD, BACK}
            The direction to travel in.
        duration : float
            How many seconds to travel for.
        """
        super(LinearMovement, self).__init__(drone)
        self._pid_alt = PID(KP, KI, KP, setpoint=f.DEFAULT_ALTITUDE)
        self._count = duration * (1.0/c.DELAY_INTERVAL)
        velocities = []
        for v in direction.value:
            velocities.append(v * f.DEFAULT_SPEED)
        self._vx = velocities[0]
        self._vy = velocities[1]
        self._vz = velocities[2]

    def perform(self):
        # Get control value
        zv = -self._pid_alt(self._drone.rangefinder.distance)
        # Send 0 velocities to drone (excepting altitude correction)
        self._drone.send_velocity(self._vx, self._vy, zv)
        self._count -= 1

        return self._count <= 0


class Takeoff(TaskBase):
    """A task that takes off the drone from the ground.

    Attributes
    ----------
    _target_alt : float
        How many meters off the ground to take off to.
    """
    def __init__(self, drone, altitude):
        """Initialize a task for taking off.

        Parameters
        ----------
        drone : dronekit.Vehicle
            The drone being controlled
        altitude : float
            How many meters off the ground to take off to.
        """
        super(Takeoff, self).__init__(drone)
        self._target_alt = altitude
    def perform(self):
        if not self._drone.armed:
            self._drone.arm()

        current_altitude = self._drone.rangefinder.distance

        if current_altitude >= self._target_alt * f.PERCENT_TARGET_ALTITUDE:
            return True

        thrust = f.DEFAULT_TAKEOFF_THRUST

        self._drone.set_attitude(0, 0, 0, thrust)
        return False
