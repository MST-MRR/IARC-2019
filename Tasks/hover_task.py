# Standard Library
from time import sleep
import threading

# Ours
from task_base import TaskBase
from ..Drone.drone import Drone
from ..Utilities import constants as c

class HoverTask(TaskBase):

    def __init__(self, drone, duration=480):
        super(HoverTask, self).__init__()
        self.drone = drone
        self.movement = None
        self.stop_event = threading.Event()
        self.duration = duration # 8 minutes default
        self.done = False

    def do(self):
        if self.movement is None:
            self.movement = self.drone.hover(self.duration, self.stop_event)
        elif self.movement.is_set():
            self.done = True
            return True

        return False

    def is_done(self):
        return self.done

    def exit_task(self):
        self.stop_event.set()
        if self.movement is not None:
            return self.movement
        else:
            cancel_event = threading.Event()
            cancel_event.set()
            return cancel_event
