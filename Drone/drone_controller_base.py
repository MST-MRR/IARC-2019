# Standard Library
import abc
import heapq
import threading

class DroneControllerBase():
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
    task: subclass of TaskBase
        Represents what the drone is doing now
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, drone):
        self.drone = drone
        self.id = None # Once we have multiple drones, this will need to be set
        self.instruction_queue = []
        self.current_instruction = None
        self.task = None

    # Attempts to establish a connection with the swarm controller
    def connect_to_swarm(self):
        """
        Behavior of this function is currently undefined.
        """
        pass

    # Lets the swarm controller know that an instruction is finished
    def notify_instruction_finished(self, instructionId):
        """
        Behavior of this function is currently undefined.
        """
        # Asynchronously let the swarm controller know that the instruction with
        # the given id has completed
        pass

    @abc.abstractmethod
    def read_next_instruction(self):
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
    def set_id(self):
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
