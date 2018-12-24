# Standard Library
import coloredlogs
import constants as c
from lock import SharedLock
import logging
import threading
from time import sleep

def init_emergency_land_event():
    """
    Returns the threading.Event that is to be passed to a drone
    controller upon its initialization and well as to the
    start_safety_loop function
    """
    return threading.Event()

# 
def start_safety_loop(emergency_land_event):
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
    SharedLock.getLock().acquire()
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='DEBUG')
    logger.info(threading.current_thread().name + ": Safety loop started")
    SharedLock.getLock().release()
    while True:
        try:
            # If the controller thread does not exist, it must have returned and so it is
            # deduced that it is time for the program to exit
            if "ControllerThread" not in [t.getName() for t in threading.enumerate()]:
                logger.info(threading.current_thread().name + ": All thread except main have finished - Program exiting")
                exit()
            sleep(c.HALF_SEC)
        except KeyboardInterrupt:
            logger.warning(threading.current_thread().name + ": Emergency Landing Initiated")
            # Set the event flag
            emergency_land_event.set()
            logger.info(threading.current_thread().name + ": Waiting for response from controller")
            count = 0 # Used as a timeout variable
            # Wait for the controller to 'respond' (clear the event flag)
            while emergency_land_event.is_set():
                sleep(c.HUNDRED_MILI)
                count += c.HUNDRED_MILI
                if count >= 5 * c.SECOND: # 5 seconds (Should this be increased for safety?)
                    logger.warning(threading.current_thread().name + ": Controller not responding - Program exiting")
                    exit()
            # The flag has been clear
            logger.info(threading.current_thread().name + ": Controller has responded")
            # Now wait for it to be set again, indicating the emergency landing has finished
            if emergency_land_event.wait(timeout=10) is True:
                logger.info(threading.current_thread().name + ": Emergency landing successful - Program exiting")
            else:
                logger.warning(threading.current_thread().name + ": Emergency landing may have failed (controller never said it landed) - Program exiting")
            exit()