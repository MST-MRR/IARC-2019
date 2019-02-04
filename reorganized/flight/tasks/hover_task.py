from task_base import TaskBase
from .. import constants as c

class HoverTask(TaskBase):
    def __init__(self, drone, altitude, duration):
        super(HoverTask, self).__init__(drone)
        self._movement = None
        self._duration = duration # 8 minutes default

    def perform(self):
        if self._movement is None:
            self._movement = self._drone.hover(self._duration, self._stop_event)
        elif self._movement.is_set():
            self._done = True
            return True

        return False
