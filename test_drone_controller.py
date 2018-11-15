from drone_controller import DroneController
from test_drone import TestDrone

class TestDroneController(DroneController):
    def setId(self):
        return 1

    def setDrone(self):
        self.drone = TestDrone()

    # This is the complicated part. It decides the logic of how
    # the drone is controlled. This implementation is not a good
    # example.
    def update(self):
        if not self.movementQueue:
            return False

        direction, distance = self.movementQueue.popleft()
        print ("Starting move...")
        self.drone.move(direction, distance=distance)
        print("Finished move...")
        return True

    def readNextInstruction(self):
        super(TestDroneController, self).readNextInstruction()
