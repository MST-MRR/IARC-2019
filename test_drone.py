from drone import Drone
import constants as c

class TestDrone(Drone):
    def move(self, direction, velocity = c.DEFAULT_VELOCITY, duration = 1, distance = None):
        super(TestDrone, self).move(direction, velocity, duration, distance)

    def loadDevices(self):
        pass