from drone_base import DroneBase
from ..Utilities import constants as c

class Drone(DroneBase):
    def move(self, direction, velocity = c.DEFAULT_VELOCITY, duration = 1, distance = None):
        super(Drone, self).move(direction, velocity, duration, distance)

    def loadDevices(self):
        pass