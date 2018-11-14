from Drone import Drone

class MovementInstructionReader(object):

    # Simple method of getting to (x, y, z) relative to start
    def readMovementInstruction(self, i, movementQueue):
        (x, y, z) = i.payload

        if x is not 0:
            movementQueue.append((Drone.BACKWARD if x > 0 else Drone.FORWARD, abs(x)))

        if y is not 0:
            movementQueue.append((Drone.LEFT if y > 0 else Drone.RIGHT, abs(y)))

        if z is not 0:
            movementQueue.append((Drone.UP if z > 0 else Drone.DOWN, abs(z)))
