
from task_base import TaskBase

DEGREE_BUFFER = .5 #acceptable error of angle in degrees

class Yaw(TaskBase):
    """
    A task to make the drone yaw to a given heading either relative or absolute.

    Attributes
    ----------
    _has_started : bool
        Indicates whether the drone has started to yaw.
    _new_heading : int
        Stores the given heading after modding it by 360 to keep it in range.
    _yaw_speed : int
        The speed in degrees/sec that the drone performs the yaw.
    _yaw_direction : int
        The direction which you force the drone rotoate: -1 for counterclockwise, and 1 for clockwise.
    __relative : bool
        Stores whether the given heading is relative or absolute: True means relative and False means absolute.
    """
    def __init__(self, drone, heading, yaw_speed=0, yaw_direction=1, relative=True):
        """
        Initialize a task for yawing.

        Parameters
        ----------
        drone : dronekit.Vehicle
            The drone being controlled.
        heading : int
            The heading for the drone to go to.
        yaw_speed : int
            The degrees/sec that the drone performs the yaw: defaults to 0.
        yaw_direction : int
            The direction which the drone should yaw, same as _yaw_direction: defaults to 1.
        relative : bool
            The status whether the passed heading is relative or absolute, same as _relative: defaults to True.
        """
        super(Yaw, self).__init__(drone)
        self._has_started = False
        self._new_heading = heading%360
        self._yaw_speed = yaw_speed
        self._yaw_direction = yaw_direction
        self._relative = relative

    def perform(self):
        """Do one iteration of logic for yawing the drone."""
        if not self._has_started:
            self.start_heading = self._drone.heading
            self._drone.send_yaw(self._new_heading, self._yaw_speed, self._yaw_direction, self._relative)
            self._has_started = True
        elif ((not self._relative and abs(self._drone.heading - self._new_heading) > DEGREE_BUFFER) or 
                (self._relative and abs(self._drone.heading - self.start_heading) < self._new_heading - DEGREE_BUFFER)):
            return False
        else:
            return True