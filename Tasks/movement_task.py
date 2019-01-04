# Standard Library
from collections import deque
import threading

# Ours
from task_base import TaskBase
from ..Drone.drone import Drone
from ..Utilities import constants as c

class MovementTask(TaskBase):

    def __init__(self, drone, movement_queue):
        super(MovementTask, self).__init__()
        self.currentMovement = None
        self.stop_event = threading.Event()
        self.drone = drone
        self.movement_queue = movement_queue
        self.done = False

    def do(self):
        # If there is not current movement and the queue is not empty,
        # pop the queue and start the movement
        if self.currentMovement is None and len(self.movement_queue):
            direction, distance = self.movement_queue.popleft()
            self.currentMovement = self.drone.move(direction, distance, self.stop_event)

        # If current movement is still none, we ran out of movements and are done    
        if self.currentMovement is None:
            self.done = True
            return True
        # If the movement is finished, set current movement to none
        elif self.currentMovement.is_set():
            # Reset the current movement and allow a new movement to begin
            self.currentMovement = None

        return False

    def is_done(self):
        return self.done

    def exit_task(self):
        self.stop_event.set()

        if self.currentMovement is not None:
            return self.currentMovement
        else:
            cancel_event = threading.Event()
            cancel_event.set()
            return cancel_event

