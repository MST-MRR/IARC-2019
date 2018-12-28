# Standard Library
from collections import deque

# Ours
from task_base import TaskBase
from ...Instructions.Movement.movement import Movement
from ...Utilities import constants as c
from ...Utilities.two_way_event import TwoWayEvent

class MovementTask(TaskBase):

    def __init__(self):
        super(MovementTask, self).__init__()
        self.currentMovement = None
        self.movement_queue = deque()
        self.state = c.ACTIVE

    def do(self):
        # If there is an active movement happening, check to see if it has finished
        if self.currentMovement is None and len(self.movement_queue):
            direction, distance = self.movement_queue.popleft()
            self.currentMovement = Movement(path=(direction, distance))
            self.currentMovement.start() # start movement thread

        # If current movement is still none, we ran out of movements and are done    
        if self.currentMovement is None:
            self.state = c.FINISHED
            return

        # Process remaining movements
        elif self.currentMovement.get_state() is c.FINISHED:
            # Reset the current movement and allow a new movement to begin
            self.currentMovement = None

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

    def get_movement_queue(self):
        """
        Returns the movement queue

        Parameters
        ----------
        None

        Returns:
        ----------
        deque
        """
        return self.movement_queue
