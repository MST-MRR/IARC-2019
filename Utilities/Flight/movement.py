# Standard Library
import coloredlogs
import logging
import threading
import time

# Ours
from ...Drone.drone import Drone
from ...Utilities import constants as c
from ...Utilities.Safety.drone_exceptions import BadArgumentException
from ...Utilities.two_way_event import TwoWayEvent

class Movement(threading.Thread):
    """
    Represents a single movement that the drone makes

    Data Members
    ----------
    drone: drone.Drone
        Interface to the drone
    type: PATH, HOVER, TAKEOFF, or LAND (see constants.py)
        Represents the type of movement being requested
    state: ACTIVE, FINISHED, CANCELED, or PAUSED (see constants.py)
        Represents the state of the movement - ACTIVE means the movement
        is happening now, FINISHED means the movement has finished, 
        CANCELED means the movement is currently processing
        a cancellation request, PAUSED is currently undefined
    stop_event: threading.Event
        Set whenever a cancellation has been requested
    """

    id = 1

    def __init__(self, **kwargs):
        """
        kwargs: Dictionary
        Exactly one of the following key value pairs must be given:
            path=(DIRECTION, DISTANCE)
                where DIRECTION is UP, DOWN, LEFT, RIGHT, FORWARD, BACK (see constants.py)
                and DISTANCE is a Double
            hover=DURATION
                where DURATION is an Integer
            takeoff=TARGET_ALTITUDE
                where TARGET_ALTITUDE is a Double
            land=True
                the value does not matter
        """
        self.logger = logging.getLogger(__name__)
      
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
        self.setName("MovementThread-" + str(Movement.id))
        Movement.id += 1
        self.drone = Drone.getDrone()
        self.state = c.ACTIVE
        self.stop_event = TwoWayEvent()
        self.done_event = threading.Event()

    def get_state(self):
        """
        Getter for self.state

        Parameters
        ----------
        None

        Returns:
        ----------
        ACTIVE, FINISHED, CANCELED, or PAUSED (see constants.py)
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
        self.state = c.FINISHED
        self.done_event.set()
            
    def runPath(self):
        """
        Wraps Drone.move()

        Returns:
        ----------
        None
        """
        self.logger.info(threading.current_thread().name + ": Starting move")
        self.drone.move(self.direction, self.distance, self.stop_event)
        self.logger.info(threading.current_thread().name + ": Finished move")

    def runHover(self):
        """
        Wraps Drone.hover()

        Returns:
        ----------
        None
        """
        self.logger.info(threading.current_thread().name + ": Starting hover (" + str(self.duration) + "s)")
        self.drone.hover(self.duration, self.stop_event)
        self.logger.info(threading.current_thread().name + ": Finished hover")

    def runTakeoff(self):
        """
        Wraps Drone.takeoff()

        Returns:
        ----------
        None
        """
        self.logger.info(threading.current_thread().name + ": Starting takeoff")
        if self.drone.takeoff(self.target_altitude, self.stop_event):
            self.logger.info(threading.current_thread().name + ": Finished takeoff")
        else:
            self.logger.info(threading.current_thread().name + ": Aborted takeoff")
    
    def runLand(self):
        """
        Wraps Drone.land()

        Returns:
        ----------
        None
        """
        self.logger.info(threading.current_thread().name + ": Starting land")
        self.drone.land()
        self.logger.info(threading.current_thread().name + ": Finished land")

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
        Stop event which is set when the movement has been canceled
        """
        if self.type is c.LAND:
            self.warning(threading.current_thread().name + ": Cannot cancel a land movement! Land proceeding")

        self.stop_event.set_m()
        
        return self.stop_event

    # TODO
    def pause(self):
        """
        Behavior of this function is currently undefined.
        """
        self.state = c.WAITING

    def get_done_event(self):
        """
        Returns an event which is set when the movement
        is done.

        Parameters
        ----------
        None

        Returns:
        ----------
        threading.Event
        """
        return self.done_event
    
