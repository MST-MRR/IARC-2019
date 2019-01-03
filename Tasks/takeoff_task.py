# Ours
from ..Drone.drone import Drone
from task_base import TaskBase
from ..Utilities import constants as c
from ..Utilities.two_way_event import TwoWayEvent

class TakeoffTask(TaskBase):

    def __init__(self, alt):
        super(TakeoffTask, self).__init__()
        self.drone = Drone.getDrone()
        self.cancel_event = TwoWayEvent()
        self.target_alt = alt
        self.movement = None
        self.state = c.ACTIVE

    def do(self):
        if self.movement is None:
            self.movement = self.drone.Movement(takeoff=self.target_alt)
            self.movement.start()
        elif self.movement.get_state() is c.FINISHED:
            self.state = c.FINISHED

    def is_done(self):
        if self.state is c.FINISHED:
            return True
        else:
            return False

    def exit_task(self):
        return self.movement.cancel()
