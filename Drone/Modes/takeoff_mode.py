# Standard Library
from time import sleep

# Ours
from ..drone import Drone
from mode_base import ModeBase
from ...Instructions.Movement.movement import Movement
from ...Utilities import constants as c
from ...Utilities.two_way_event import TwoWayEvent

class TakeoffMode(ModeBase):

    def __init__(self, alt):
        super(TakeoffMode, self).__init__()
        self.drone = Drone.getDrone()
        self.cancel_event = TwoWayEvent()
        self.target_alt = alt
        self.movement = None
        self.state = c.ACTIVE

    def do(self):
        if self.movement is None:
            self.movement = Movement(takeoff=self.target_alt)
            self.movement.start()
        elif self.movement.get_state() is c.FINISHED:
            self.state = c.FINISHED

    def is_done(self):
        if self.state is c.FINISHED:
            return True
        else:
            return False

    def exit_mode(self):
        return self.movement.cancel()
