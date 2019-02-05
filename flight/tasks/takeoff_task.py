from task_base import TaskBase
from .. import constants as c

class TakeoffTask(TaskBase):
    """A task that takes off the drone from the ground."""
    def __init__(self, drone, altitude):
        """Initialize a task for taking off.

        Parameters
        ----------
        drone : dronekit.Vehicle
            The drone being controlled
        altitude : double
            How many meters off the ground to take off to.
        """
        super(TakeoffTask, self).__init__(drone)
        self._target_alt = altitude

    def perform(self):
        current_altitude = self._drone.rangefinder.distance

        if current_altitude >= self._target_alt * c.PERCENT_TARGET_ALTITUDE:
            return True

        thrust = c.DEFAULT_TAKEOFF_THRUST

        self._drone.set_attitude(0, 0, 0, thrust)
        return False
