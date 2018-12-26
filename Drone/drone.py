# Ours
from drone_base import DroneBase
from ..Utilities import constants as c

class Drone(DroneBase):
    """
    Concrete implementation of DroneBase. See drone__base.py for
    documentation.
    """
    drone = None

    @staticmethod
    def getDrone():
        if Drone.drone is None:
            Drone.drone = Drone()

        return Drone.drone

    def move(self, direction, velocity = c.DEFAULT_VELOCITY, duration = 1, distance = None):
        super(Drone, self).move(direction, velocity, duration, distance)

    def loadDevices(self):
        pass