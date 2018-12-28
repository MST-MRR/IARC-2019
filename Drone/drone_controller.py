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
from Tasks.takeoff_task import TakeoffTask
from Tasks.hover_task import HoverTask
from ..Utilities import constants as c
from ..Utilities.drone_exceptions import EmergencyLandException
from ..Utilities.lock import SharedLock

class DroneController(DroneControllerBase):
    """
    Concrete implementation of DroneControllerBase. See drone_controller_base.py for
    documentation.
    """
    def __init__(self):
        super(DroneController, self).__init__()
        self.logger = logging.getLogger(__name__)
        coloredlogs.install(level='DEBUG')
        # The following two lines are purely for testing purposes. Instructions
        # will be pushed onto the heap as a result of the swarm controller
        # sending instructions or inter-drone communication.
        heapq.heappush(self.instruction_queue, (0, MovementInstruction(2, 0, 0)))
        #heapq.heappush(self.instruction_queue, (0, MovementInstruction(-5, -5, 0)))

    def setId(self):
        return 1

    def update(self):
        try:
            # Check to see if emergency landing has been initiated
            if self.emergency_land_event.is_set_m():
                # Acknowledge that the event has been seen
                self.emergency_land_event.set_a()
                raise EmergencyLandException("Keyboard interrupt")
            
            if self.task is not None:
                # Do one iteration of whichever task we are in
                self.task.do()

                # If we are done, set the task to None so that 
                # we can move on to the next instruction
                if self.task.is_done():
                    self.task = None

            if type(self.task) is HoverTask or self.task is None:
                # Process remaining instructions
                if len(self.instruction_queue):
                    # Stop hovering, if we were doing so
                    if type(self.task) is HoverTask:
                        stop_hover_event = self.task.exit_task()
                        stop_hover_event.wait_r()
                        self.task = None
                    self.readNextInstruction()
                # If there are no instructions, begin to hover
                else:
                    if self.task is None:
                        self.task = HoverTask()

            # NOTE: this implementation never returns True and so never
            # returns True on its own - the user must initiate landing
            # with ctrl-c
            return False
        except Exception as e:
            # Print stack trace for non keyboard interupts
            if type(e) is not EmergencyLandException:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback)

            # If a connection was never establish in the first place, return
            if self.drone.vehicle is None:
                return True

            # If currently have a task, exit it
            if self.task is not None and not self.task.is_done():
                exit_event = self.task.exit_task()
                # timeout included because movement tasks sometimes failed to cancel
                # if they were less than a second away from completing
                exit_event.wait_r(timeout=1) 

            land = Movement(land=True)
            land.start()
            land.get_done_event().wait()
            self.emergency_land_event.set_r()

            return True

    def run(self):
        SharedLock.getLock().acquire()
        self.logger.info(threading.current_thread().name + ": Controller thread started")
        SharedLock.getLock().release()

        try:
            # Connect to low-level controller
            self.drone.connect(isInSimulator = True)
            
            # Arm the drone for flight
            self.drone.arm()
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
        
        # Set up a takeoff task
        self.task = TakeoffTask(alt=1)

        while True:
            if self.update():
                self.logger.info(threading.current_thread().name + ": Controller thread stopping")
                # Give other threads some time
                return
            sleep(c.HALF_SEC)
        
    def readNextInstruction(self):
        super(DroneController, self).readNextInstruction()
