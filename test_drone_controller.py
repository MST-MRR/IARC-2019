from drone_controller import DroneController
from test_drone import TestDrone
import constants as c
from time import sleep
import threading
import heapq
from movement_instruction import MovementInstruction
from movement import Movement

class TestDroneController(DroneController):
    def __init__(self, drone, emergency_land_event):
        super(TestDroneController, self).__init__(drone, emergency_land_event)
        self.currentMovement = None
        heapq.heappush(self.instructionQueue, (0, MovementInstruction(5, 5, 0)))
        heapq.heappush(self.instructionQueue, (0, MovementInstruction(-5, -5, 0)))

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

        # If there is an active movement happening, wait
        if self.currentMovement is not None:
            if self.currentMovement.state is c.ACTIVE:
                sleep(c.HALF_SEC)
            elif self.currentMovement.state is c.DEFAULT:
                self.currentMovement = None
                print threading.current_thread().name, ": Starting hover"
                self.drone.hover(5)
                print threading.current_thread().name, ": Hover complete"
        # Process remaining movements before next instruction
        elif len(self.movementQueue):
            direction, distance = self.movementQueue.popleft()
            self.currentMovement = Movement(self.drone, direction, distance)
            self.currentMovement.start() # start movement thread
        elif len(self.instructionQueue):
            self.readNextInstruction()
        else:
            print "GOT HERE"
            return False # All finished

        # Check to see if emergency landing has been initiated
        if self.emergency_land_event.isSet():
            # Acknowledge that the event has been seen
            self.emergency_land_event.clear()
            # If a movement is going on, cancel it
            if self.currentMovement is not None:
                self.currentMovement.cancel()
            # There may be a delay since movement is happening in a different thread
            while self.currentMovement.state is not c.CANCELED:
                print "GOT HERE"
                sleep(c.TEN_MILI)
            # No movements are happening, so start landing
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
        print threading.current_thread().name, ": Controller thread started"
        while True:
            if not self.update():
                return
        print threading.current_thread().name, ": Controller thread stopping"

    def readNextInstruction(self):
        super(TestDroneController, self).readNextInstruction()
