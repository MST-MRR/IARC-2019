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
            sleep(c.HALF_SEC)
        except KeyboardInterrupt:
            print threading.current_thread().name, ": Emergency Landing Initiated"
            emergency_land_event.set()
            print threading.current_thread().name, ": Waiting for response from controller"
            while emergency_land_event.is_set():
                sleep(c.HUNDRED_MILI)
            print threading.current_thread().name, ": Controller has responded"
            emergency_land_event.wait()
            print threading.current_thread().name, ": Emergency landing complete - Program exiting"
            exit()