from drone import Drone

class MovementInstructionReader(object):

    # Simple method of getting to (x, y, z) relative to start
    def readMovementInstruction(self, i, movementQueue):
        (x, y, z) = i.payload

        if x != 0:
            movementQueue.append((Drone.BACKWARD if x > 0 else Drone.FORWARD, abs(x)))

        if y != 0:
            movementQueue.append((Drone.LEFT if y > 0 else Drone.RIGHT, abs(y)))

        if z != 0:
            movementQueue.append((Drone.UP if z > 0 else Drone.DOWN, abs(z)))
