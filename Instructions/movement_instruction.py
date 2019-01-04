from collections import deque

# Ours
from ..Tasks.movement_task import MovementTask
from instruction_base import InstructionBase
from ..Utilities import constants as c

class MovementInstruction(InstructionBase):

    def __init__(self, data):
        super(MovementInstruction, self).__init__()
        # The data here will eventually be the raw binary data that
        # has traveled over the network. The decoding may be more
        # involved than what is shown here.
        (self.x, self.y, self.z) = data
        
        self.movementTask = None

    def get_task(self, drone):
        queue = deque()
        if self.x != 0:
            queue.append((c.BACKWARD if self.x > 0 else c.FORWARD, abs(self.x)))

        if self.y != 0:
            queue.append((c.LEFT if self.y > 0 else c.RIGHT, abs(self.y)))

        if self.z != 0:
            queue.append((c.UP if self.z > 0 else c.DOWN, abs(self.z)))

        self.movementTask = MovementTask(drone, queue)

        return self.movementTask
