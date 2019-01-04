# Standard Library
import threading

# Ours
from ..Drone.drone import Drone
from task_base import TaskBase
from ..Utilities import constants as c

class TakeoffTask(TaskBase):

    def __init__(self, drone, alt):
        super(TakeoffTask, self).__init__()
        self.drone = drone
        self.stop_event = threading.Event()
        self.target_alt = alt
        self.movement = None
        self.done = False

    def do(self):
        if self.movement is None:
            self.movement = self.drone.takeoff(self.target_alt, self.stop_event)
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
