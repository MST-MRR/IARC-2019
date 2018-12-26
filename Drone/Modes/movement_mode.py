# Standard Library
from collections import deque
from time import sleep

# Ours
from mode_base import ModeBase
from ...Instructions.Movement.movement import Movement
from ...Utilities import constants as c
from ...Utilities.two_way_event import TwoWayEvent

class MovementMode(ModeBase):

    def __init__(self):
        super(MovementMode, self).__init__()
        self.currentMovement = None
        self.movement_queue = deque()
        self.state = c.ACTIVE

    def do(self):
        # If there is an active movement happening...
        if self.currentMovement is not None:
            # Check to see if it is active - if so, wait
            if self.currentMovement.get_state() is c.ACTIVE:
                sleep(c.HALF_SEC)
            # Else, the movement must be finished
            elif self.currentMovement.get_state() is c.FINISHED:
                # Reset the current movement and allow a new movement to begin
                self.currentMovement = None
        # Process remaining movements
        elif len(self.movement_queue):
            direction, distance = self.movement_queue.popleft()
            self.currentMovement = Movement(path=(direction, distance))
            self.currentMovement.start() # start movement thread
        else:
            self.state = c.FINISHED

    def is_done(self):
        if self.state is c.FINISHED:
            return True
        else:
            return False

    def exit_mode(self):
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
