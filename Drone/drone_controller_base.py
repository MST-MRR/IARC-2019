# Standard Library
import abc
import heapq
import threading

# Ours
from ..Utilities.Safety.drone_exceptions import NetworkException
from ..Utilities.Safety.emergency_land import EmergencyLand

class DroneControllerBase(threading.Thread):
    """
    Responsible for managing the execution of tasks, maintaining a queue of
    instructions, and responding gracefully to emergency landing events.

    Data Members
    ----------
    id: Integer
        Identification number used by the swarm controller
        to distinguish between the drones
    instruction_queue: list of InstructionBase subclass 
        A priority queue holding instruction sent from the
        swarm controller or interdrone communication
    current_instruction: subclass of InstructionBase
        The instruction currently being processed
    emergency_land_event: TwoWayEvent
        Event which is set when an emergency landing is requested,
        as when a keyboard interrupt comes in
    task: subclass of TaskBase
        Represents what the drone is doing now
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(DroneControllerBase, self).__init__()
        self.setName("ControllerThread") # Set name of thread for ease of debugging
        self.id = None # Once we have multiple drones, this will need to be set
        self.instruction_queue = []
        self.current_instruction = None
        self.emergency_land_event = EmergencyLand.get_emergency_land_event()
        self.task = None

    # Attempts to establish a connection with the swarm controller
    def connectToSwarm(self):
        """
        Behavior of this function is currently undefined.
        """
        pass

    # Lets the swarm controller know that an instruction is finished
    def notifyInstructionFinished(self, instructionId):
        """
        Behavior of this function is currently undefined.
        """
        # Asynchronously let the swarm controller know that the instruction with
        # the given id has completed
        pass

    @abc.abstractmethod
    def readNextInstruction(self):
        """
        Discards the old instruction and sets current_instruction to the next instruction
        in self.instruction_queue. Calls the get_task method on the new instruction and
        sets task to the value returned.

        Parameters
        ----------
        None

        Precondition:
        ----------
        The instruction queue is not empty.

        Postcondition:
        ----------
        The instruction queue contains one less element.

        Returns:
        ----------
        None
        """
        pass

    @abc.abstractmethod
    def setId(self):
        """
        Sets the drone's id

        Parameters
        ----------
        None

        Postcondition:
        ----------
        self.id is set to some unique value

        Returns:
        ----------
        None
        """
        self.id = 0


    @abc.abstractmethod
    def update(self):
        """
        Checks that a land event has not been set and executes the
        next iteration of the current task, if one exists

        Returns:
            False if the update should continue to be called.
            True if update should stop being called.
        """
        pass
 
    @abc.abstractmethod
    def run(self):
        """
        Method overriden from threading.Thread. The start() method calls this method.
        https://docs.python.org/2/library/threading.html. Responsible for connecting
        and arming the drone, and waiting for the update loop to signal it is finished.
        """
        pass