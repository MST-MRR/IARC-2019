import threading
import constants as c
import time
from drone_exceptions import BadArgumentException

class Movement(threading.Thread):
    def __init__(self, drone, **kwargs):
        for kind, arg in kwargs.items():
            if kind == "path":
                self.type = c.PATH
                self.direction = arg[0]
                self.distance = arg[1]
            elif kind == "hover":
                self.type = c.HOVER
                self.duration = arg
            elif kind == "takeoff":
                self.type = c.TAKEOFF
                self.target_altitude = arg
            elif kind == "land":
                self.type = c.LAND
            else:
                raise BadArgumentException("Movement(): Must give path, hover, \
                    takeoff, or land as argument")
            
        super(Movement, self).__init__()
        self.setName("MovementThread")
        self.drone = drone
        self.state = c.DEFAULT
        self.stop_event = threading.Event()

    def get_state(self):
        return self.state

    def get_type(self):
        return self.type

    # Called when self.Start() is called
    def run(self):
        if self.type == c.PATH:
            self.runPath()
        elif self.type == c.HOVER:
            self.runHover()
        elif self.type == c.TAKEOFF:
            self.runTakeoff()
        elif self.type == c.LAND:
            self.runLand()
            
    def runPath(self):
        print threading.current_thread().name, ": Starting move"
        self.state = c.ACTIVE
        self.drone.move(self.direction, self.distance, self.stop_event)
        self.state = c.DEFAULT
        print threading.current_thread().name, ": Finished move"

    def runHover(self):
        print threading.current_thread().name, ": Starting hover (", self.duration, "s)"
        self.state = c.ACTIVE
        self.drone.hover(self.duration, self.stop_event)
        self.state = c.DEFAULT
        print threading.current_thread().name, ": Finished hover"

    def runTakeoff(self):
        print threading.current_thread().name, ": Starting takeoff"
        self.state = c.ACTIVE
        self.drone.takeoff(self.target_altitude, self.stop_event)
        self.state = c.DEFAULT
        print threading.current_thread().name, ": Finished takeoff"
    
    def runLand(self):
        print threading.current_thread().name, ": Starting land"
        self.state = c.ACTIVE
        self.drone.land()
        self.state = c.DEFAULT
        print threading.current_thread().name, ": Finished land"

    def cancel(self):
        if self.type is c.LAND:
            print threading.current_thread().name, ": Cannot cancel a land movement! Land proceeding"

        self.stop_event.set()
        one_pass = False
        while self.stop_event.isSet():
            time.sleep(c.SECOND)
            # In the event that the cancel is requested during the last second
            # of send_global_velocity's execution, the isSet flag will never be
            # cleared. If a second has passed (the frequency of send_global_velocity 
            # loop), then it is deduced that this is the situation, and we can break.
            if one_pass:
                break
            one_pass = True

        self.state = c.CANCELED

    # TODO
    def pause(self):
        self.state = c.WAITING
    
