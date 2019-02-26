"""Constructs and destructs tasks that the drone controller can perform."""

from flight.tasks import Exit, Land, Takeoff, TakeoffSim, Hover, LinearMovement
import flight.constants as constants
import config

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


# The width in characters of each field
FIELD_WIDTH = 2

EMPTY_FIELD = '00'

# Map direction encoding to Direction enum
ENCODING_TO_DIRECTION = {
    '00':   constants.Directions.UP,
    '01':   constants.Directions.DOWN,
    '02':   constants.Directions.LEFT,
    '03':   constants.Directions.RIGHT,
    '04':   constants.Directions.FORWARD,
    '05':   constants.Directions.BACKWARD
}

# Map Direction enum to direction encoding
DIRECTION_TO_ENCODING = {
    constants.Directions.UP: '00',
    constants.Directions.DOWN: '01',
    constants.Directions.LEFT: '02',
    constants.Directions.RIGHT: '03',
    constants.Directions.FORWARD: '04',
    constants.Directions.BACKWARD: '05'
}

# Map priority encoding to Priority enum
ENCODING_TO_PRIORITY = {
    '00':   constants.Priorities.LOW,
    '01':   constants.Priorities.MEDIUM,
    '02':   constants.Priorities.HIGH
}

# Map Priority enum to priority encoding
PRIORITY_TO_ENCODING = {
    constants.Priorities.LOW: '00',
    constants.Priorities.MEDIUM: '01',
    constants.Priorities.HIGH: '02'
}

class TaskFactory(object):
    """Creates Task objects from binary input.

    Attributes
    ----------
    _drone : flight.drone.Drone
        The drone that tasks are being created for.
    """

    def __init__(self, drone=None):
        """Initialize a task factory.

        Parameters
        ----------
        drone : flight.drone.Drone, optional
            The drone that tasks are being created for. If a drone object is
            not supplied, the decode function will not be usable.
        """
        self._drone = drone

    def exit_task_encode(self, priority=constants.Priorities.HIGH):
        """Translates parameters into an encoded exit task.

        Parameters
        ----------
        priority : constants.Priorities
            Priority at which the task should be executed.
        """
        priority_encoding = PRIORITY_TO_ENCODING[priority]
        num_empty = 6
        return "{}{}{}".format(TASK_EXIT,
                               priority_encoding,
                               EMPTY_FIELD*num_empty).upper()

    def land_task_encode(self, priority=constants.Priorities.MEDIUM):
        """Translates parameters into an encoded land task.

        Parameters
        ----------
        priority : constants.Priorities
            Priority at which the task should be executed.

        """
        priority_encoding = PRIORITY_TO_ENCODING[priority]
        num_empty = 6
        return "{}{}{}".format(TASK_LAND,
                               priority_encoding,
                               EMPTY_FIELD*num_empty).upper()

    def takeoff_task_encode(self, altitude=config.DEFAULT_ALTITUDE,
                                priority=constants.Priorities.MEDIUM):
        """Translates parameters into an encoded takeoff task.

        Parameters
        ----------
        priority : constants.Priorities
            Priority at which the task should be executed.
        altitude : int
            Altitude to takeoff to.
        """
        priority_encoding = PRIORITY_TO_ENCODING[priority]
        num_empty = 5
        return "{}{}{:02x}{}".format(TASK_TAKEOFF,
                                    priority_encoding,
                                    altitude,
                                    EMPTY_FIELD*num_empty).upper()

    def linear_movement_task_encode(self, duration, direction,
            altitude=config.DEFAULT_ALTITUDE, priority=constants.Priorities.MEDIUM):
        """Translates parameters into an encoded linear movement task.

        Parameters
        ----------
        priority : constants.Priorities
            Priority at which the task should be executed.
        duration : int
            How long in seconds to move in the specified direction.
        altitude : int
            The altitude at which to remain while moving.
        """
        priority_encoding = PRIORITY_TO_ENCODING[priority]
        duration_encoding = hex(duration).upper()
        direction_encoding = DIRECTION_TO_ENCODING[direction]
        altitude_encoding = alt_encoding = hex(altitude).upper()
        num_empty = 3
        return "{}{}{:02x}{}{:02x}{}".format(TASK_LINEAR_MOVEMENT,
                                        priority_encoding,
                                        duration,
                                        direction_encoding,
                                        altitude,
                                        EMPTY_FIELD*num_empty).upper()

    def hover_task_encode(self, duration, altitude=config.DEFAULT_ALTITUDE,
                            priority=constants.Priorities.MEDIUM):
        """Translates parameters into an encoded hover task.

        Parameters
        ----------
        priority : constants.Priorities
            Priority at which the task should be executed.
        duration : int
            How long in seconds to hover.
        altitude : int
            The altitude at which to hover.
        """
        priority_encoding = PRIORITY_TO_ENCODING[priority]
        duration_encoding = hex(duration).upper()
        altitude_encoding = alt_encoding = hex(altitude).upper()
        num_empty = 4
        return "{}{}{:02x}{:02x}{}".format(TASK_LINEAR_MOVEMENT,
                                        priority_encoding,
                                        duration,
                                        altitude,
                                        EMPTY_FIELD*num_empty).upper()

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
                priority = ENCODING_TO_PRIORITY[priority_field]
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
        print self._drone.is_simulation
        if self._drone.is_simulation:
            task = TakeoffSim(self._drone, altitude)
        else:
            task = Takeoff(self._drone, altitude)
        return task

    def linear_movement_task_decode(self, msg):
        """Decodes data into a LinearMovement task.

        Parameters
        ----------
        msg : str
            The msg to be translated into a task.
        """
        duration = int(msg[FIELD_3:FIELD_3 + FIELD_WIDTH], 16)
        direction = ENCODING_TO_DIRECTION[msg[FIELD_4:FIELD_4 + FIELD_WIDTH]]
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
