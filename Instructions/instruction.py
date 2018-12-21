import uuid
import abc

class Instruction(object):
    """
    Base class that represent an instruction created by a swarm controller
    and followed by a drone controller

    Data Members
    ----------
    id: uuid.uuid4
        Identification number for the instruction (used by swarm controller
        to distinguish between the instructions it sends out)
    droneId: Integer
        Identification number of the drone controller the instruction is meant
        for (used to double check that the drone that receives the message is
        the one who want meant to receive it)
    timeout: Integer
        Time in seconds, after which the second should be discarded
    payload: Abstract
        The core data of the instruction which is defined by objects that are
        children of this class
    """
    __metaclass__ = abc.ABCMeta

    # Set the id 
    def __init__(self, timeout = 10):
        # Unique id of the instruction for book keeping
        self.id = uuid.uuid4()
        # ID of the drone used to ensure a drone does not read
        # an instruction meant for another drone
        self.droneId = None
        # If the instruction is not finished by this time, assume it failed
        self.timeout = timeout

    @abc.abstractproperty
    def payload(self):
        return