from simple_pid import PID

from task_base import TaskBase
from .. import constants as c

class HoverTask(TaskBase):
    def __init__(self, drone, altitude, duration):
        super(HoverTask, self).__init__(drone)
        self._duration = duration
        self._pid_alt = PID(1, 0.1, 0.05, setpoint=altitude)
        self._count = duration * (1.0/c.DELAY_INTERVAL)

    def perform(self):
        # Get control value
        zv = -self._pid_alt(self._drone.rangefinder.altitude)
        # Send 0 velocities to drone (excepting altitude correction)
        self._drone.send_velocity(0, 0, zv)
        self._count -= 1

        if self._count <= 0:
            return True
        else:
            return False
