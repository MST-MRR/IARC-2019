from Drone import Drone

class TestDrone(Drone):
    def backward(self, velocity = Drone.DEFAULT_VELOCITY, duration = 1, distance = None):
        super(TestDrone, self).backward(velocity, duration, distance)

    def forward(self, velocity = Drone.DEFAULT_VELOCITY, duration = 1, distance = None):
        super(TestDrone, self).forward(velocity, duration, distance)

    def left(self, velocity = Drone.DEFAULT_VELOCITY, duration = 1, distance = None):
        super(TestDrone, self).forward(velocity, duration, distance)

    def right(self, velocity = Drone.DEFAULT_VELOCITY, duration = 1, distance = None):
        super(TestDrone, self).right(velocity, duration, distance)

    def up(self, velocity = Drone.DEFAULT_VELOCITY, duration = 1, distance = None):
        super(TestDrone, self).up(velocity, duration, distance)

    def down(self, velocity = Drone.DEFAULT_VELOCITY, duration = 1, distance = None):
        super(TestDrone, self).down(velocity, duration, distance)

    def loadDevices(self):
        pass