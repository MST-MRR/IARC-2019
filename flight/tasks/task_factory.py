"""Constructs and destructs tasks that the drone controller can perform."""

from flight.tasks import Exit, Land, Takeoff, Hover, LinearMovement
import flight.constants as constants

class BadParams(Exception):
    pass

# For future use, perhaps
"""
TASK_HOVER = 0b00000000

TASK_LAND = 0b00000001

TASK_TAKEOFF = 0b00000010

TASK_LINEAR_MOVEMENT = 0b00000011

TASK_HOVER = 0b00000100
"""

# Tasks to ID

TASK_EXIT = '00'

TASK_LAND = '01'

TASK_TAKEOFF = '02'

TASK_LINEAR_MOVEMENT = '03'

TASK_HOVER = '04'

# Fields starting indeces

FIELD_1 = 0

FIELD_2 = 2

FIELD_3 = 4

FIELD_4 = 6

FIELD_5 = 8

FIELD_6 = 10

FIELD_7 = 12

FIELD_8 = 14

FIELD_WIDTH = 2

# Map direction encoding to Direction enum
DIRECTION_MAP = {
    '00':   constants.Directions.UP,
    '01':   constants.Directions.DOWN,
    '02':   constants.Directions.LEFT,
    '03':   constants.Directions.RIGHT,
    '04':   constants.Directions.FORWARD,
    '05':   constants.Directions.BACKWARD
}

# Map priority encoding to Priority enum
PRIORITY_MAP = {
    '00':   constants.Priorities.LOW,
    '01':   constants.Priorities.MEDIUM,
    '02':   constants.Priorities.HIGH
}

class TaskFactory(object):
    """Creates Task objects from binary input.

    Attributes
    ----------
    _drone : flight.drone.Drone
        The drone that tasks are being created for.
    """

    def __init__(self, drone):
        """Initialize a task factory.

        Parameters
        ----------
        drone : flight.drone.Drone
            The drone that tasks are being created for.
        """
        self._drone = drone

    def decode(self, msg):
        """Decodes a binary message.

        Parameters
        ----------
        msg : str
            A string of 16 characters that make up a hexadecimal number.
        """
        try:
            task_type = msg[:2]
            if task_type in TASK_TO_DECODER.keys():
                priority_field = msg[FIELD_2:FIELD_2 + FIELD_WIDTH]
                priority = PRIORITY_MAP[priority_field]
                return (priority, TASK_TO_DECODER[task_type](self, msg))
        except BadParams as e:
            print e
        except Exception as e:
            print "Unknown exception: {}".format(e)


    def exit_task_decode(self, msg):
        """Decodes data into an Exit task.

        Parameters
        ----------
        msg : str
            The msg to be translated into a task.
        """
        return Exit(self._drone)


    def land_task_decode(self, msg):
        """Decodes data into a Land task.

        Parameters
        ----------
        msg : str
            The msg to be translated into a task.
        """
        return Land(self._drone)

    def takeoff_task_decode(self, msg):
        """Decodes data into a Takeoff task.

        Parameters
        ----------
        msg : str
            The msg to be translated into a task.
        """
        altitude = int(msg[FIELD_3:FIELD_3 + FIELD_WIDTH], 16)
        return Takeoff(self._drone, altitude)

    def linear_movement_task_decode(self, msg):
        """Decodes data into a LinearMovement task.

        Parameters
        ----------
        msg : str
            The msg to be translated into a task.
        """
        duration = int(msg[FIELD_3:FIELD_3 + FIELD_WIDTH], 16)
        direction = DIRECTION_MAP[msg[FIELD_4:FIELD_4 + FIELD_WIDTH]]
        return LinearMovement(self._drone, direction, duration)

    def hover_task_decode(self, msg):
        """Decodes data into a Hover task.

        Parameters
        ----------
        msg : str
            The msg to be translated into a task.
        """
        duration = int(msg[FIELD_3:FIELD_3 + FIELD_WIDTH], 16)
        altitude = int(msg[FIELD_4:FIELD_4 + FIELD_WIDTH], 16)
        return Hover(self._drone, altitude, duration)

# Maps task ID to a function that decodes a binary message for that task
TASK_TO_DECODER = {
    TASK_EXIT:    TaskFactory.exit_task_decode,
    TASK_LAND:    TaskFactory.land_task_decode,
    TASK_TAKEOFF:    TaskFactory.takeoff_task_decode,
    TASK_LINEAR_MOVEMENT:    TaskFactory.linear_movement_task_decode,
    TASK_HOVER:    TaskFactory.hover_task_decode
}
