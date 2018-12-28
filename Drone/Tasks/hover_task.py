# Standard Library
from time import sleep

# Ours
from task_base import TaskBase
from ...Instructions.Movement.movement import Movement
from ...Utilities import constants as c
from ...Utilities.two_way_event import TwoWayEvent

class HoverTask(TaskBase):

    def __init__(self, duration=480):
        super(HoverTask, self).__init__()
        self.currentMovement = None
        self.done_event = None
        self.state = c.ACTIVE
        self.duration = duration # 8 minutes default

    def do(self):
        if self.currentMovement is None:
            self.currentMovement = Movement(hover=self.duration)
            self.currentMovement.start()
            self.done_event = self.currentMovement.get_done_event()
        elif self.done_event.is_set():
            self.state = c.FINISHED

    def is_done(self):
        if self.state is c.FINISHED:
            return True
        else:
            return False

    def exit_task(self):
        if self.currentMovement is not None:
            cancel_event = self.currentMovement.cancel()
        else:
            cancel_event = TwoWayEvent()
            cancel_event.set_r()
        return cancel_event
