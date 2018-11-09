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
            print ("Starting move...")
            self.drone.move(direction, distance = distance)
            print("Finished move...")
            print("Starting 5 second hover...")
            self.drone.set_attitude(duration = 5)
            print("Hover finished.")
            return True
        else:
            return False

    def readNextInstruction(self):
        super(TestDroneController, self).readNextInstruction()
