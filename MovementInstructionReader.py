class MovementInstructionReader(object):

    # Simple method of getting to (x, y, z) relative to start
    def readMovementInstruction(self, i, movementQueue):
        (x, y, z) = i.payload
        if x > 0:
            movementQueue.append(('backward', x))
        elif x < 0:
            movementQueue.append(('forward', -1 * x))

        if y > 0:
            movementQueue.append(('left', y))
        elif y < 0:
            movementQueue.append(('right', -1 * y))

        if z > 0:
            movementQueue.append(('up', z))
        elif z < 0:
            movementQueue.append(('down', -1 * z))
