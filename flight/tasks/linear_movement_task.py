from task_base import TaskBase
from simple_pid import PID
from flight import constants as c
from flight import flightconfig as f

KP = 1
KI = 0
KD = 0

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
