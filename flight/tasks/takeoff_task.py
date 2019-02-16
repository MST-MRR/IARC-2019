from task_base import TaskBase
from .. import constants as c
from ... import flightconfig as f

class TakeoffTask(TaskBase):
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
        super(TakeoffTask, self).__init__(drone)
        self._target_alt = altitude
        self._count = 10 / c.DELAY_INTERVAL
        self._began_takeoff = False
    def perform(self):
        if not self._drone.armed:
            self._drone.arm()
        elif not self._began_takeoff:
            print "HERE"
            self._drone.simple_takeoff(self._target_alt)
            self._began_takeoff = True
        else:
            self._count -= 1

        if self._count <= 0:
            return True
        else:
            return False
