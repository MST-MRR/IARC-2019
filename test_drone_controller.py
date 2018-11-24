from drone_controller import DroneController
from test_drone import TestDrone
import constants as c
from time import sleep
import threading
import heapq
from movement_instruction import MovementInstruction
from movement import Movement
import sys
from drone_exceptions import EmergencyLandException
import traceback

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
        try:
            if not self.drone.is_connected():
                self.drone.connect(isInSimulator = True)
            
            if not self.drone.is_armed():
                self.drone.arm()

            if not self.drone.is_flying() and not self.drone.is_taking_off():
                self.currentMovement = Movement(self.drone, takeoff=1)
                self.currentMovement.start()

            # If there is an active movement happening...
            if self.currentMovement is not None:
                # Check to see if it is active - if so, wait
                if self.currentMovement.get_state() is c.ACTIVE:
                    sleep(c.HALF_SEC)
                # Else, the movement must be finished and in its default state
                elif self.currentMovement.get_state() is c.DEFAULT:
                    # If the movement was along a path, start to hover
                    if self.currentMovement.get_type() is c.PATH:
                        self.currentMovement = Movement(self.drone, hover=3)
                        self.currentMovement.start()
                    # Reset the current movement and allow a new movement to begin
                    else:
                        self.currentMovement = None
            # Process remaining movements
            elif len(self.movementQueue):
                direction, distance = self.movementQueue.popleft()
                self.currentMovement = Movement(self.drone, path=(direction, distance))
                self.currentMovement.start() # start movement thread
            # Process remaining instructions (notice movements are always 
            # processed before instructions, if they exist)
            elif len(self.instructionQueue):
                self.readNextInstruction()
            # If this line is reached, all the instructions have been processed
            else:
                self.currentMovement = Movement(self.drone, land=True)
                self.currentMovement.start()
                # Wait for land to finish - it will hold up the thread, but everything
                # has been completed anyway
                self.currentMovement.join()
                return False # All finished

            # Check to see if emergency landing has been initiated
            if self.emergency_land_event.isSet():
                # Acknowledge that the event has been seen
                self.emergency_land_event.clear()
                raise EmergencyLandException("Keyboard interrupt")
            sleep(c.TEN_MILI)
            return True
        except Exception as e:
            print "Error encountered in", threading.current_thread().name, ":"
            print "\tType:", type(e)
            print "\tMessage:", e
            print traceback.print_exc()
            # If a connection was never establish in the first place, return
            if self.drone.vehicle is None:
                return False
            # If a movement is going on, cancel it
            if self.currentMovement is not None:
                self.currentMovement.cancel()
                # There may be a delay since movement is happening in a different thread
                while self.currentMovement.state is not c.CANCELED:
                    sleep(c.TEN_MILI)
            # No movements are happening, so start landing
            self.drone.land()
            self.emergency_land_event.set()
            return False
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
                print threading.current_thread().name, ": Controller thread stopping"
                return
        

    def readNextInstruction(self):
        super(TestDroneController, self).readNextInstruction()
