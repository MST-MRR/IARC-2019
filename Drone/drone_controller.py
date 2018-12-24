# Standard Library
import coloredlogs
import heapq
import logging
import threading
from time import sleep
import traceback
import sys

# Ours
from drone import Drone
from drone_controller_base import DroneControllerBase
from ..Instructions.Movement.movement_instruction import MovementInstruction
from ..Instructions.Movement.movement import Movement
from ..Utilities import constants as c
from ..Utilities.drone_exceptions import EmergencyLandException
from ..Utilities.failsafe_controller import FailsafeController
from ..Utilities.lock import SharedLock

class DroneController(DroneControllerBase):
    """
    Concrete implementation of DroneController. See drone_controller.py for
    documentation.
    """
    def __init__(self, drone, emergency_land_event):
        super(DroneController, self).__init__(drone, emergency_land_event)
        self.currentMovement = None
        self.logger = logging.getLogger(__name__)
        coloredlogs.install(level='DEBUG')
        # These lines are purely for testing purposes. Once swarm controller and
        # the networking thread are implemented, this sort of function call will
        # likely be done in update(), after checking that new instruction have
        # arrived over the network.
        heapq.heappush(self.instruction_queue, (0, MovementInstruction(5, 5, 0)))
        heapq.heappush(self.instruction_queue, (0, MovementInstruction(-5, -5, 0)))

    def setId(self):
        return 1

    def update(self):
        try:
            # If not connected, try to connect
            if not self.drone.is_connected():
                self.drone.connect(isInSimulator = True)
            
            # If not armed, try to arm
            if not self.drone.is_armed():
                self.drone.arm()

            # If not flying, try to fly
            if not self.drone.is_flying() and not self.drone.is_taking_off():
                self.currentMovement = Movement(self.drone, takeoff=1)
                self.currentMovement.start()

            # If there is an active movement happening...
            if self.currentMovement is not None:
                # Check to see if it is active - if so, wait
                if self.currentMovement.get_state() is c.ACTIVE:
                    sleep(c.HALF_SEC)
                # Else, the movement must be finished
                elif self.currentMovement.get_state() is c.FINISHED:
                    # If the movement was along a path, start to hover
                    if self.currentMovement.get_type() is c.PATH:
                        self.currentMovement = Movement(self.drone, hover=3)
                        self.currentMovement.start()
                    # Reset the current movement and allow a new movement to begin
                    else:
                        self.currentMovement = None
            # Process remaining movements
            elif len(self.movement_queue):
                direction, distance = self.movement_queue.popleft()
                self.currentMovement = Movement(self.drone, path=(direction, distance))
                self.currentMovement.start() # start movement thread
            # Process remaining instructions (movements are  
            # processed before instructions, if they exist)
            elif len(self.instruction_queue):
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

    def run(self):
        SharedLock.getLock().acquire()
        self.logger.info(threading.current_thread().name + ": Controller thread started")
        SharedLock.getLock().release()
        fscontroller = FailsafeController(self.drone)
        fsevent = fscontroller.get_failesafe_event()
        fscontroller.start()
        while True:
            if not self.update():
                self.logger.info(threading.current_thread().name + ": Controller thread stopping")
                return
            if fsevent.is_set():
                self.emergency_land_event.set()
                fsevent.clear()
        
    def readNextInstruction(self):
        super(DroneController, self).readNextInstruction()
