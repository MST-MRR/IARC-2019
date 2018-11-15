import uuid
import abc

class Instruction(object):
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