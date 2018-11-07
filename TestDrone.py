from Drone import Drone

class TestDrone(Drone):
    def backward(self, velocity, duration):
        super(Drone, self).backward(velocity, duration)

    def backward(self, distance):
        super(Drone, self).backward(distance)

    def forward(self, velocity, duration):
        super(Drone, self).forward(velocity, duration)

    def forward(self, distance):
        super(Drone, self).forward(distance)

    def left(self, velocity, duration):
        super(Drone, self).forward(velocity, duration)

    def forward(self, distance):
        super(Drone, self).forward(distance)

    def right(self, velocity, duration):
        super(Drone, self).right(velocity, duration)

    def right(self, distance):
        super(Drone, self).right(distance)

    def up(self, velocity, duration):
        super(Drone, self).up(velocity, duration)

    def up(self, distance):
        super(Drone, self).up(distance)

    def down(self, velocity, duration):
        super(Drone, self).down(velocity, duration)

    def down(self, distance):
        super(Drone, self).down(distance)

    def loadDevices(self):
        pass