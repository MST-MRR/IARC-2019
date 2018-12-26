# Standard Library
import abc

# Ours
from ..instruction import Instruction


class MovementInstruction(Instruction):
    """
    The payload of a MovementInstruction is (currently) defined as follows:
        (Double, Double, Double)
    which represent the x, y, and z coordinate the drone is meant
    to fly to as if the current location were the origin
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @property
    def payload(self):
        return (self.x, self.y, self.z)