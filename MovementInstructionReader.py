from Drone import Drone

class MovementInstructionReader(object):

    # Simple method of getting to (x, y, z) relative to start
    def readMovementInstruction(self, i, movementQueue):
        (x, y, z) = i.payload
        if x > 0:
            movementQueue.append((Drone.BACKWARD, x))
        elif x < 0:
            movementQueue.append((Drone.FORWARD, x))

        if y > 0:
            movementQueue.append((Drone.LEFT, y))
        elif y < 0:
            movementQueue.append((Drone.RIGHT, y))

        if z > 0:
            movementQueue.append((Drone.UP, z))
        elif z < 0:
            movementQueue.append((Drone.DOWN, z))
