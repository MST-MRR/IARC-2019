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
from ..Instructions.movement_instruction import MovementInstruction
from ..Tasks.hover_task import HoverTask
from ..Tasks.movement_task import MovementTask
from ..Tasks.takeoff_task import TakeoffTask
from ..Utilities import constants as c
from ..Utilities import drone_exceptions as de
from ..Utilities.lock import SharedLock

class DroneController(DroneControllerBase):
    """
    Concrete implementation of DroneControllerBase. See drone_controller_base.py for
    documentation.
    """
    def __init__(self, drone):
        super(DroneController, self).__init__(drone)
        self.logger = logging.getLogger(__name__)
        self.debug = False
        coloredlogs.install(level='DEBUG')
        # The following two lines are purely for testing purposes. Instructions
        # will be pushed onto the heap as a result of the swarm controller
        # sending instructions or inter-drone communication.
        heapq.heappush(self.instruction_queue, (0, MovementInstruction((5, 5, 0))))
        heapq.heappush(self.instruction_queue, (0, MovementInstruction((-5, -5, 0))))

    def set_id(self):
        return 1

    def update(self):
        if self.task is not None:
            # Do one iteration of whichever task we are in
            result = self.task.do()

            # If we are done, set the task to None so that 
            # we can move on to the next instruction
            if result:
                self.task = None

        if type(self.task) is HoverTask or self.task is None:
            # Process remaining instructions
            if len(self.instruction_queue):
                # Stop hovering, if we were doing so
                if type(self.task) is HoverTask:
                    stop_hover_event = self.task.exit_task()
                    stop_hover_event.wait()
                    self.task = None
                self.read_next_instruction()
            # If there are no instructions, begin to hover
            else:
                if self.task is None:
                    self.task = HoverTask(self.drone)
         
    def run_loop(self):
        SharedLock.getLock().acquire()
        self.logger.info(threading.current_thread().name + ": Main control loop starting")
        SharedLock.getLock().release()

        try:
            # Connect to low-level controller
            self.drone.connect(isInSimulator = True)
            
            # Arm the drone for flight
            self.drone.arm()
         
            # Set up a takeoff task
            self.task = TakeoffTask(self.drone, 1)

            # NOTE: the only way to stop the loop is to raise an exceptions, such
            # as with a keyboard interrupt
            while True:
                self.do_safety_checks()
                self.update()
                sleep(c.SHORT_INTERVAL)

        except BaseException as e:
            self.logger.warning(threading.current_thread().name + ": Emergency Landing Initiated")
            # Only print stack trace for completely unexpected things
            self.logger.critical(type(e).__name__)
            if self.debug is True:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)

            # If a connection was never establish in the first place, return
            if not self.drone.is_connected():
                return True

            # If currently have a task, exit it
            if self.task is not None and not self.task.is_done():
                exit_event = self.task.exit_task()
                exit_event.wait() 

            # Land the drone
            land = self.drone.land()
            land.wait()
            self.logger.info(threading.current_thread().name + ": Landing complete - main control loop stopping")
        
    def read_next_instruction(self):
        if len(self.instruction_queue):      
            self.current_instruction = heapq.heappop(self.instruction_queue)[1]
            self.task = self.current_instruction.get_task(self.drone)

    def do_safety_checks(self):
        if not self.drone.connected:
            return

        if self.drone.vehicle.airspeed > c.VELOCITY_THRESHOLD:
            raise de.VelocityExceededThreshold()
            
        if self.drone.vehicle.location.global_relative_frame.alt > c.MAXIMUM_ALLOWED_ALTITUDE:
            raise de.AltitudeExceededThreshold()

        if self.drone.vehicle.rangefinder.distance < c.RANGEFINDER_MIN - c.RANGEFINDER_EPSILON -.5:
            raise de.RangefinderMalfunction()

        # TODO: Add more safety checks here
