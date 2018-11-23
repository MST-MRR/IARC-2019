import threading
from time import sleep
import constants as c

def init_emergency_land_event():
    return threading.Event()

# Periodically checks to see if a keyboard interrupt has happened.
# If so, it notifies the controller (which has a reference to the
# event). The controller then resets the event, initiates a landing,
# and sets the event once the landing has completed, at which point
# the program exits. 
def start_safety_loop(emergency_land_event):
    print threading.current_thread().name, ": Safety loop started"
    while True:
        try:
            if "ControllerThread" not in [t.getName() for t in threading.enumerate()]:
                print threading.current_thread().name, ": All thread except main have finished - Program exiting"
                exit()
            sleep(c.HALF_SEC)
        except KeyboardInterrupt:
            print threading.current_thread().name, ": Emergency Landing Initiated"
            emergency_land_event.set()
            print threading.current_thread().name, ": Waiting for response from controller"
            count = 0 # Used as a timeout variable
            while emergency_land_event.is_set():
                sleep(c.HUNDRED_MILI)
                count += c.HUNDRED_MILI
                if count >= 5 * c.SECOND: # 5 seconds
                    print threading.current_thread().name, ": Controller not responding - Program exiting"
                    exit()
            print threading.current_thread().name, ": Controller has responded"
            if emergency_land_event.wait(timeout=10) is True:
                print threading.current_thread().name, ": Emergency landing successful - Program exiting"
            else:
                print threading.current_thread().name, ": Emergency landing may have failed (controller never said it landed) - Program exiting"
            exit()