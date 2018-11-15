from drone import Drone
import constants as c

class MovementInstructionReader(object):

    # Simple method of getting to (x, y, z) relative to start
    def readMovementInstruction(self, i, movementQueue):
        (x, y, z) = i.payload

        if x != 0:
            movementQueue.append((c.BACKWARD if x > 0 else c.FORWARD, abs(x)))

        if y != 0:
            movementQueue.append((c.LEFT if y > 0 else c.RIGHT, abs(y)))

        if z != 0:
            movementQueue.append((c.UP if z > 0 else c.DOWN, abs(z)))
