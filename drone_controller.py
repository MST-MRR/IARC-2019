import abc
import heapq
from movement_instruction_reader import MovementInstructionReader
from movement_instruction import MovementInstruction
from drone import Drone
from collections import deque
from drone_exceptions import NetworkError


# Every drone controller will know how to read movement instructions
class DroneController(MovementInstructionReader):
    __metaclass__ = abc.ABCMeta

    def __init__(self, drone):
        self.id = None # should the drone set its own id or should the swarm controller give an id?
        self.master = None # Will be set to an IP address here
        self.drone = drone
        self.instructionQueue = []
        self.currentInstruction = None
        self.movementQueue = deque()

    # Attempts to establish a connection with the swarm controller
    def connectToSwarm(self):
        if self.master is None or self.id is None:
            raise NetworkError("IP address of master or id of this controller has not been set!")
        else:
            # Establish TCP or otherwise connection with the swarm controller
            pass

    

    # Lets the swarm controller know that an instruction is finished
    def notifyInstructionFinished(self, instructionId):
        # Asynchronously let the swarm controller know that the instruction with
        # the given id has completed
        pass

    # Starts networking thread, which is responsible for asynchronously sending
    # and receiving messages, as well as alerting this object that a new instruction
    # has arrived
    def startNetworkThread(self):
        pass

    # Starts the update thread, which is responsible for repeatedly calling update
    def startUpdateThread(self):
        pass

    def landAndTerminate(self):
        self.drone.land()
        # Stop threads

    def takeoff(self, altitude):
        self.drone.takeoff(altitude)

    # Discards the old instruction and sets currentInstruction to the next instruction
    # of highest priority. Will be customized based on what kind of instructions the
    # concrete instance of drone controller can interpret
    @abc.abstractmethod
    def readNextInstruction(self):
        if len(self.instructionQueue) > 0:      
            self.currentInstruction = heapq.heappop(self.instructionQueue)[1]
            # If it is a movement instruction
            if type(self.currentInstruction) is MovementInstruction:
                self.readMovementInstruction(self.currentInstruction, self.movementQueue)
            # If it is a ??? instruction and so on (there will be different instruction readers
            # which know how to interpret and act on different instructions)
        else:
            # enter idle state (needs to be implemented)
            pass

    # The concrete drone controller subclass must implement a method to set
    # its own id.
    @abc.abstractmethod
    def setId(self):
        self.id = 0

    # Takes the next best action to control the drone. Responible for carrying
    # out new instructions as needed and notifying when instructions have been
    # finished. Also responsible for collision avoidance.
    @abc.abstractmethod
    def update(self):
        pass