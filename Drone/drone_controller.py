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
from Modes.takeoff_mode import TakeoffMode
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
            
            # Check to see if emergency landing has been initiated
            if self.emergency_land_event.is_set_m():
                # Acknowledge that the event has been seen
                self.emergency_land_event.set_a()
                raise EmergencyLandException("Keyboard interrupt")
            
            # If not connected, try to connect
            if not self.drone.is_connected():
                self.drone.connect(isInSimulator = True)
            
            # If not armed, try to arm
            if not self.drone.is_armed():
                self.drone.arm()

            # If not flying, try to fly
            if not self.drone.is_taking_off() and not self.drone.is_flying() and self.mode is None:
                self.mode = TakeoffMode(alt=1)

            # Remove takeoff mode once the drone is flying
            if self.drone.is_flying() and type(self.mode) == TakeoffMode:
                self.mode = None
            
            if self.mode is not None:
                # Do one iteration of whichever mode we are in
                self.mode.do()

                # If we are done, set the mode to None so that 
                # we can move on to the next instruction
                if self.mode.is_done():
                    self.mode = None
            else:
                # Process remaining instructions
                if len(self.instruction_queue):
                    # Stop hovering, if we were doing so
                    if self.no_mode_hover is not None:
                        stop_hover_event = self.no_mode_hover.cancel()
                        stop_hover_event.wait_r()
                        self.no_mode_hover = None
                    SharedLock.getLock().acquire()
                    self.readNextInstruction()
                    SharedLock.getLock().release()
                else:
                    # Hover until asn instruction comes in or landing
                    # is requested
                    # TODO - Have Movement land drone if hover finishes its 
                    # full time (pass flag to indicate this behavior)
                    if self.no_mode_hover is None:
                        self.no_mode_hover = Movement(hover=60)
                        self.no_mode_hover.start()
                    sleep(c.HALF_SEC)

            # Keep going (NOTE: this implementation never returns True and so never
            # returns on its own - the user must tell the drone to land with ctrl-c)
            return False
        except Exception as e:
            # No need print traceback of a keyboard interrupt
            if type(e) is not EmergencyLandException:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback)
            # If a connection was never establish in the first place, return
            if self.drone.vehicle is None:
                return True
            # If currently in a mode, exit it
            if self.mode is not None and not self.mode.is_done():
                exit_event = self.mode.exit_mode()
                exit_event.wait_r(timeout=1)
            # If we weren't in a mode and were hovering, stop hovering
            elif self.no_mode_hover is not None:
                stop_hover_event = self.no_mode_hover.cancel()
                stop_hover_event.wait_r()

            land = Movement(land=True)
            land.start()
            land.get_done_event().wait()
            self.emergency_land_event.set_r()
            return True

    def run(self):
        SharedLock.getLock().acquire()
        self.logger.info(threading.current_thread().name + ": Controller thread started")
        SharedLock.getLock().release()
        
        while True:
            if self.update():
                self.logger.info(threading.current_thread().name + ": Controller thread stopping")
                return
        
    def readNextInstruction(self):
        super(DroneController, self).readNextInstruction()
