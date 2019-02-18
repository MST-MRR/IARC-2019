from task_base import TaskBase
from .. import constants as c
from ... import flightconfig as f

class TakeoffTask(TaskBase):
    """A task that takes off the drone from the ground. This task is intended
    for use on the real drone only.

    Attributes
    ----------
    _target_alt : float
        How many meters off the ground to take off to.
    _count : int
        Keeps track of how many more iterations this task should be called on
        before it returns true (i.e. finished).
    _began_takeoff : bool
        Set to true after the drone has been armed but not yet finished takeoff.

    Notes
    -----
    This task will not work on the simulated drone.
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
        super(TakeoffTask, self).__init__(drone)
        self._target_alt = altitude
        self._count = 10 / c.DELAY_INTERVAL
        self._began_takeoff = False

    def perform(self):
        if not self._drone.armed:
            self._drone.arm()
        elif not self._began_takeoff:
            self._drone.simple_takeoff(self._target_alt)
            self._began_takeoff = True
        else:
            self._count -= 1

        if self._count <= 0:
            return True
        else:
            return False
