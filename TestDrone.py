from Drone import Drone

class TestDrone(Drone):
    def move(self, direction, velocity = Drone.DEFAULT_VELOCITY, duration = 1, distance = None):
        super(TestDrone, self).move(direction, velocity, duration, distance)

    def loadDevices(self):
        pass