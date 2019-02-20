from task_base import TaskBase
from .. import constants as c
from ... import flightconfig as f

class TakeoffTaskSim(TaskBase):
    """A task that takes off the drone from the ground (meant for simulator).

    Attributes
    ----------
    _target_alt : float
        How many meters off the ground to take off to.

    Notes
    -----
    This method of takeoff is unstable on the real drone.
    """
    def __init__(self, drone, altitude, roll=0, pitch=0, yaw=0):
        """Initialize a task for taking off.
        Parameters
        ----------
        drone : dronekit.Vehicle
            The drone being controlled
        altitude : float
            How many meters off the ground to take off to.
        """
        super(TakeoffTaskSim, self).__init__(drone)
        self._target_alt = altitude
        self._roll = roll
        self._pitch = pitch
        self._yaw = yaw

    def perform(self):
        if not self._drone.armed:
            self._drone.arm()

        current_altitude = self._drone.rangefinder.distance

        if current_altitude >= self._target_alt * f.PERCENT_TARGET_ALTITUDE:
            return True

        thrust = f.DEFAULT_TAKEOFF_THRUST

        self._drone.set_attitude(self._roll, self._pitch, self._yaw, thrust)
        return False
