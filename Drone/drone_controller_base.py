# Standard Library
import abc
import heapq
import threading

# Ours
from drone import Drone
from ..Instructions.Movement.movement_instruction_reader import MovementInstructionReader
from ..Instructions.Movement.movement_instruction import MovementInstruction
from Tasks.movement_task import MovementTask
from ..Utilities.drone_exceptions import NetworkException
from ..Utilities.emergency_land import EmergencyLand

# Every drone controller will know how to read movement instructions
class DroneControllerBase(MovementInstructionReader, threading.Thread):
    """
    Responsible for processing instructions received from the swarm controller 
    along with drone sensor data to best control the movement and actions of 
    a drone in accordance with the goal of the mission.

    Data Members
    ----------
    id: Integer
        Identification number used by the swarm controller
        to distinguish between the drones
    drone: drone.Drone
        Interface for controlling the drone
    instruction_queue: list of instruction.Instruction
        A priority queue holding instruction send from the
        swarm controller
    current_instruction: instruction.Instruction
        The instruction currently being processed
    movement_queue: list of movement.Movement
        List of path movements the drone should make.
    emergency_land_event: threading.Event
        Event which is set when an emergency landing is requested,
        as when a keyboard interrupt comes in
    task: one of MOVEMENT, FOLLOW, HEAL, or DECODE (see constants)
        Determines the behavior of the controller
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(DroneControllerBase, self).__init__()
        self.setName("ControllerThread") # Set name of thread for ease of debugging
        self.id = None # Once we have multiple drones, this will need to be set
        self.drone = Drone.getDrone()
        self.instruction_queue = []
        self.current_instruction = None
        self.emergency_land_event = EmergencyLand.get_emergency_land_event()
        self.task = None

    # Attempts to establish a connection with the swarm controller
    def connectToSwarm(self):
        """
        Behavior of this function is currently undefined.
        """
        if self.master is None or self.id is None:
            raise NetworkException("IP address of master or id of this controller has not been set!")
        else:
            # Establish TCP or otherwise connection with the swarm controller
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
        in self.instruction_queue. Should be customized to match the kinds of instructions
        a particular kind of drone controller can read (i.e. which XXXInstructionReader it
        is a subclass of)

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
        if len(self.instruction_queue):      
            self.current_instruction = heapq.heappop(self.instruction_queue)[1]
            if type(self.current_instruction) is MovementInstruction:
                self.task = MovementTask()
        
                # The following method is inherited from MovementInstructionReader
                self.readMovementInstruction(self.current_instruction, self.task.get_movement_queue())
            # In the future, there may be other types of instruction (other than movements) we
            # want to process here (for example, HealInstruction)

    @abc.abstractmethod
    def setId(self):
        """
        Hardcoded setter for drone ID

        Parameters
        ----------
        None

        Returns:
        ----------
        None
        """
        self.id = 0


    @abc.abstractmethod
    def update(self):
        """
        Takes the next best action to control the drone. Responsible for connecting, arming,
        and taking off the drone, carrying out instructions as needed, and safely landing 
        the drone (whether due to mission completed or emergency). 

        Returns:
            True if the update should continue to be called.
            False if update should stop being called.
        """
        pass
 
    @abc.abstractmethod
    def run(self):
        """
        Method overriden from threading.Thread. The start() method calls this method.
        https://docs.python.org/2/library/threading.html. When this function finishes,
        the thread ends.
        """
        pass