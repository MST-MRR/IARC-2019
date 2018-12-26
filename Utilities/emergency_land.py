# Standard Library
import coloredlogs
import constants as c
from lock import SharedLock
import logging
import threading
from time import sleep

# Ours
from two_way_event import TwoWayEvent
from ..Utilities.safety_checks import SafetyChecking

class EmergencyLand:

    # Static variable
    emergency_land_event = None

    # Follows singleton design pattern
    @staticmethod
    def get_emergency_land_event():
        """
        Returns a threading.Event. If the event has not yet been created,
        it is created.
        """
        if EmergencyLand.emergency_land_event is None:
            EmergencyLand.emergency_land_event = TwoWayEvent()
        
        return EmergencyLand.emergency_land_event

    @staticmethod
    def start_safety_net():
        """
        Periodically checks to see if a keyboard interrupt has happened.
        If so, it notifies the controller (which has a reference to the
        event). The controller then resets the event, initiates a landing,
        and sets the event once the landing has completed, at which point
        the program exits. 

        Parameters
        ----------
        emergency_land_event: threading.Event
            Set whenever a keyboard interrupt comes in

        Precondition:
        ----------
        None

        Postcondition:
        ----------
        The program exits.

        Returns:
        ----------
        None
        """
        emergency_land_event = EmergencyLand.get_emergency_land_event()

        SharedLock.getLock().acquire()
        logger = logging.getLogger(__name__)
        
        coloredlogs.install(level='DEBUG')
        logger.info(threading.current_thread().name + ": Safety loop started")
        SharedLock.getLock().release()

        safety_checks = SafetyChecking()
        unsafe_event = safety_checks.get_safety_check_event()
        safety_checks.start()
        
        while True:
            try:
                # If the controller thread does not exist, it must have returned and so it is
                # deduced that it is time for the program to exit
                if "ControllerThread" not in [t.getName() for t in threading.enumerate()]:
                    logger.info(threading.current_thread().name + ": All thread except main have finished - Program exiting")
                    exit()
                # Check that nothing wacky is happening
                if unsafe_event.is_set_m():
                    unsafe_event.set_a()
                    raise Exception("Unsafe Condition")
                sleep(c.HALF_SEC)
            except (KeyboardInterrupt, Exception) as e:
                logger.warning(threading.current_thread().name + ": Emergency Landing Initiated")
                # Signal to the controller that an emergency landing has been requested
                emergency_land_event.set_m()
                logger.info(threading.current_thread().name + ": Waiting for response from controller")
                # Wait for the controller to respond
                if emergency_land_event.wait_a(timeout=5):
                    logger.info(threading.current_thread().name + ": Controller has responded")
                    # Now wait for it to be set again, indicating the emergency landing has finished
                    if emergency_land_event.wait_r(timeout=30):
                        logger.info(threading.current_thread().name + ": Emergency landing successful - Program exiting")
                    else:
                        logger.warning(threading.current_thread().name + ": Emergency landing may have failed (controller never said it landed) - Program exiting")
                    exit()
                else:
                    logger.warning(threading.current_thread().name + ": Controller not responding - Program exiting")
                    exit()
                
                