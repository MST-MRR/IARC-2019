# Ours
from ...Drone.drone import Drone
from ...Utilities import constants as c

class MovementInstructionReader(object):
    """
    Capable of interpretting MovementInstruction objects

    Data Members
    ----------
    None
    """

    def readMovementInstruction(self, i, movement_queue):
        """
        Cuts a coordinate up into a series of planar movements and adds them
        to the given movement queue

        Parameters
        ----------
        i: (Double, Double, Double)
            The coordinate to fly to as if the current location is the origin
        movement_queue: list of Movement objects
            A drone controllers movement queue (see drone_controller.py)

        Precondition:
        ----------
        None

        Postcondition:
        ----------
        movement_queue may have several items added to it

        Returns:
        ----------
        None
        """
        (x, y, z) = i.payload

        if x != 0:
            movement_queue.append((c.BACKWARD if x > 0 else c.FORWARD, abs(x)))

        if y != 0:
            movement_queue.append((c.LEFT if y > 0 else c.RIGHT, abs(y)))

        if z != 0:
            movement_queue.append((c.UP if z > 0 else c.DOWN, abs(z)))
