
from task_base import TaskBase

DEGREE_BUFFER = .5 #acceptable error of angle in degrees

class YawTask(TaskBase):
    """
    DOCSTRING
    """
    def __init__(self, drone, heading, yaw_speed=0, yaw_direction=1, relative=False):
        """
        DOCSTRING
        """
        super(YawTask, self).__init__(drone)
        self._has_started = False
        self._new_heading = heading
        self._yaw_speed = yaw_speed
        self._yaw_direction = yaw_direction
        self._relative = relative

    def perform(self):
        if not self._has_started:
            self.start_heading = self._drone.heading
            self._drone.send_yaw(self._new_heading, self._yaw_speed, self._yaw_direction, self._relative)
        elif ((not self._relative and abs(self._drone.heading - self._new_heading) > DEGREE_BUFFER) or 
                (self._relative and abs(self._drone.heading - self.start_heading) < self._new_heading - DEGREE_BUFFER)):
            return False
        else:
            return True