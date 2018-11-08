from DroneController import DroneController
from TestDrone import TestDrone

class TestDroneController(DroneController):
    def setId(self):
        return 1

    def setDrone(self):
        self.drone = TestDrone()

    # This is the complicated part. It decides the logic of how
    # the drone is controlled. This implementation is not a good
    # example.
    def update(self):
        if self.movementQueue:
            direction, distance = self.movementQueue.popleft()
            if direction == 'backward':
                self.drone.backward(distance = distance)
            elif direction == 'forward':
                self.drone.forward(distance = distance)
            elif direction == 'left':
                self.drone.left(distance = distance)
            elif direction == 'right':
                self.drone.right(distance = distance)
            elif direction == 'up':
                self.drone.up(distance = distance)
            elif direction == 'down':
                self.drone.down(distance = distance)
            else:
                raise Exception("Unrecognized movement!")
            return True
        else:
            return False

    def readNextInstruction(self):
        super(TestDroneController, self).readNextInstruction()
