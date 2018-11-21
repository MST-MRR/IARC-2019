from drone_controller import DroneController
from test_drone import TestDrone
import constants as c
from time import sleep
import threading

class TestDroneController(DroneController):
    def __init__(self, drone, emergency_land_event):
        super(TestDroneController, self).__init__(drone, emergency_land_event)

    def setId(self):
        return 1

    def setDrone(self):
        self.drone = TestDrone()

    def update(self):
        
        if not self.drone.is_connected:
            self.drone.connect(isInSimulator = True)
        
        if not self.drone.is_armed():
            self.drone.arm()

        if not self.drone.is_flying:
            self.drone.takeoff(1)

        self.drone.hover(5)

        if self.emergency_land_event.isSet():
            self.emergency_land_event.clear()
            print threading.current_thread().name, ": Starting land"
            self.drone.land()
            print threading.current_thread().name, ": Land complete"
            self.emergency_land_event.set()
            return False
        sleep(c.TEN_MILI)
        return True
        """
        if not self.movementQueue:
            return False

        direction, distance = self.movementQueue.popleft()
        print ("Starting move...")
        self.drone.move(direction, distance=distance)
        print("Finished move...")
        return True
        """

    def run(self):
        print threading.current_thread.__name__, ": Controller thread started"
        while True:
            if not self.update():
                return
        print threading.current_thread.__name__, ": Controller thread stopping"

    def readNextInstruction(self):
        super(TestDroneController, self).readNextInstruction()
