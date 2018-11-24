import threading
import constants as c
import time
from drone_exceptions import BadArgumentException

class Movement(threading.Thread):
    """
    Represents a single movement that the drone makes

    Data Members
    ----------
    drone: drone.Drone
        Interface to the drone
    kwargs: Dictionary
        Exactly one of the following key value pairs must be given:
            path=(DIRECTION, DISTANCE)
                where DIRECTION is UP, DOWN, LEFT, RIGHT, FORWARD, BACK (see constants.py)
                and DISTANCE is a Double
            hover=DURATION
                where DURATION is an Integer
            takeoff=TARGET_ALTITUDE
                where TARGET_ALTITUDE is a Double
            land=None
                the value does not matter
    type: PATH, HOVER, TAKEOFF, or LAND (see constants.py)
        Represents the type of movement being requested
    state: ACTIVE, DEFAULT, CANCELED, or PAUSED (see constants.py)
        Represents the state of the movement - ACTIVE means the movement
        is happening now, DEFAULT means the movement has just been created
        or has finished, CANCELED means the movement is currently processing
        a cancellation request, PAUSED is currently undefined
    stop_event: threading.Event
        Set whenever a cancellation has been requested
    """
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
        """
        Getter for self.state

        Parameters
        ----------
        None

        Returns:
        ----------
        ACTIVE, DEFAULT, CANCELED, or PAUSED (see constants.py)
            The state of the movement
        """
        return self.state

    def get_type(self):
        """
        Getter for self.state

        Parameters
        ----------
        None

        Returns:
        ----------
        PATH, HOVER, TAKEOFF, or LAND (see constants.py)
            The type of movement
        """
        return self.type

    # Called when self.Start() is called
    def run(self):
        """
        Called when self.Start() is called (this is the behavior or threading.Thread)
        Takes the appropriate action based on the type of movement it is

        Parameters
        ----------
        None

        Precondition:
        ----------
        None

        Postcondition:
        ----------
        The thread terminates.

        Returns:
        ----------
        None
        """
        if self.type == c.PATH:
            self.runPath()
        elif self.type == c.HOVER:
            self.runHover()
        elif self.type == c.TAKEOFF:
            self.runTakeoff()
        elif self.type == c.LAND:
            self.runLand()
            
    def runPath(self):
        """
        Wraps Drone.move()

        Returns:
        ----------
        None
        """
        print threading.current_thread().name, ": Starting move"
        self.state = c.ACTIVE
        self.drone.move(self.direction, self.distance, self.stop_event)
        self.state = c.DEFAULT
        print threading.current_thread().name, ": Finished move"

    def runHover(self):
        """
        Wraps Drone.hover()

        Returns:
        ----------
        None
        """
        print threading.current_thread().name, ": Starting hover (", self.duration, "s)"
        self.state = c.ACTIVE
        self.drone.hover(self.duration, self.stop_event)
        self.state = c.DEFAULT
        print threading.current_thread().name, ": Finished hover"

    def runTakeoff(self):
        """
        Wraps Drone.takeoff()

        Returns:
        ----------
        None
        """
        print threading.current_thread().name, ": Starting takeoff"
        self.state = c.ACTIVE
        self.drone.takeoff(self.target_altitude, self.stop_event)
        self.state = c.DEFAULT
        print threading.current_thread().name, ": Finished takeoff"
    
    def runLand(self):
        """
        Wraps Drone.land()

        Returns:
        ----------
        None
        """
        print threading.current_thread().name, ": Starting land"
        self.state = c.ACTIVE
        self.drone.land()
        self.state = c.DEFAULT
        print threading.current_thread().name, ": Finished land"

    def cancel(self):
        """
        Cancels this thread

        Parameters
        ----------
        None

        Precondition:
        ----------
        The type of movement is not LAND 

        Postcondition:
        ----------
        self.state is set to CANCELED

        Returns:
        ----------
        None
        """
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
        """
        Behavior of this function is currently undefined.
        """
        self.state = c.WAITING
    
