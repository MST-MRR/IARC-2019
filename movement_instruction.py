from instruction import Instruction
import abc

class MovementInstruction(Instruction):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @property
    def payload(self):
        return (self.x, self.y, self.z)