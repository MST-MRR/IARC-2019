from task_base import TaskBase
from .. import constants as c

class TakeoffTask(TaskBase):

    def __init__(self, drone, altitude):
        super(TakeoffTask, self).__init__(drone)
        self._target_alt = altitude

    def perform(self):
        current_altitude = self._drone.rangefinder.distance

        if current_altitude >= self._target_alt * c.PERCENT_TARGET_ALTITUDE:
            return True

        thrust = c.DEFAULT_TAKEOFF_THRUST

        self._drone.set_attitude(0, 0, 0, thrust)
        return False
