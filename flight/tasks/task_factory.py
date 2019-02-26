"""Constructs and destructs tasks that the drone controller can perform."""

import numpy as np

from flight.tasks import Exit, Land, Takeoff, TakeoffSim, Hover, LinearMovement
import flight.constants as constants
import config

class BadParams(Exception):
    pass

# Tasks to ID
TASK_EXIT = 0

TASK_LAND = 1

TASK_TAKEOFF = 2

TASK_LINEAR_MOVEMENT = 3

TASK_HOVER = 4

YAW = 5

CIRCLE = 6

MOVEMENT = 7 # Not yet implemented

# The width in bytes of each field
FIELD_WIDTH = 2

# Fields starting indeces
FIELD_0 = FIELD_WIDTH * 0

FIELD_1 = FIELD_WIDTH * 1

FIELD_2 = FIELD_WIDTH * 2

FIELD_3 = FIELD_WIDTH * 3

FIELD_4 = FIELD_WIDTH * 4

FIELD_5 = FIELD_WIDTH * 5

FIELD_6 = FIELD_WIDTH * 6

FIELD_7 = FIELD_WIDTH * 7

EMPTY_FIELD = np.int16(0).tobytes() # 16 bits

# Map direction encoding to Direction enum
ENCODING_TO_DIRECTION = {
    0:   constants.Directions.UP,
    1:   constants.Directions.DOWN,
    2:   constants.Directions.LEFT,
    3:   constants.Directions.RIGHT,
    4:   constants.Directions.FORWARD,
    5:   constants.Directions.BACKWARD
}

# Map Direction enum to direction encoding
DIRECTION_TO_ENCODING = {
    constants.Directions.UP: 0,
    constants.Directions.DOWN: 1,
    constants.Directions.LEFT: 2,
    constants.Directions.RIGHT: 3,
    constants.Directions.FORWARD: 4,
    constants.Directions.BACKWARD: 5
}

# Map priority encoding to Priority enum
ENCODING_TO_PRIORITY = {
    0:   constants.Priorities.LOW,
    1:   constants.Priorities.MEDIUM,
    2:   constants.Priorities.HIGH
}

# Map Priority enum to priority encoding
PRIORITY_TO_ENCODING = {
    constants.Priorities.LOW: 0,
    constants.Priorities.MEDIUM: 1,
    constants.Priorities.HIGH: 2
}

def get_field(msg, field):
    return msg[field:field + FIELD_WIDTH]

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
        num_empty = 6
        msg = bytearray()
        msg += np.int16(TASK_EXIT).tobytes() # Task id
        msg += np.int16(PRIORITY_TO_ENCODING[priority]).tobytes() # Priority
        msg += EMPTY_FIELD * num_empty # Empty fields
        return msg

    def land_task_encode(self, priority=constants.Priorities.MEDIUM):
        """Translates parameters into an encoded land task.

        Parameters
        ----------
        priority : constants.Priorities
            Priority at which the task should be executed.

        """
        num_empty = 6
        msg = bytearray()
        msg += np.int16(TASK_LAND).tobytes() # Task id
        msg += np.int16(PRIORITY_TO_ENCODING[priority]).tobytes() # Priority
        msg += EMPTY_FIELD * num_empty # Empty fields
        return msg

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
        num_empty = 5
        msg = bytearray()
        msg += np.int16(TASK_TAKEOFF).tobytes() # Task id
        msg += np.int16(PRIORITY_TO_ENCODING[priority]).tobytes() # Priority
        msg += np.half(altitude).tobytes() # Altitude
        msg += EMPTY_FIELD * num_empty # Empty fields
        return msg

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
        num_empty = 3
        msg = bytearray()
        msg += np.int16(TASK_LINEAR_MOVEMENT).tobytes() # Task id
        msg += np.int16(PRIORITY_TO_ENCODING[priority]).tobytes() # Priority
        msg += np.half(duration).tobytes() # Duration
        msg += np.int16(DIRECTION_TO_ENCODING[direction]).tobytes() # Direction
        msg += np.half(altitude).tobytes() # Altitude
        msg += EMPTY_FIELD * num_empty # Empty fields
        return msg

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
        num_empty = 4
        msg = bytearray()
        msg += np.int16(TASK_HOVER).tobytes() # Task id
        msg += np.int16(PRIORITY_TO_ENCODING[priority]).tobytes() # Priority
        msg += np.half(duration).tobytes() # Duration
        msg += np.half(altitude).tobytes() # Altitude
        msg += EMPTY_FIELD * num_empty # Empty fields
        return msg

    def decode(self, msg):
        """Decodes a binary message.

        Parameters
        ----------
        msg : bytearray
            The encoded task (16 bytes long).
        """
        try:
            task_id_bytes = get_field(msg, FIELD_0)
            task_id= np.frombuffer(task_id_bytes, dtype=np.int16, count=1)[0] # returns array, take first and only element
            if task_id in TASK_TO_DECODER.keys():
                priority_id_bytes = get_field(msg, FIELD_1)
                priority_id = np.frombuffer(priority_id_bytes, dtype=np.int16, count=1)[0]
                priority = ENCODING_TO_PRIORITY[priority_id]
                return (priority, TASK_TO_DECODER[task_id](self, msg))
            else:
                raise BadParams("Invalid task id")
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
        altitude_bytes = get_field(msg, FIELD_2)
        altitude = np.frombuffer(altitude_bytes, dtype=np.half, count=1)[0]

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
        direction_id_bytes = get_field(msg, FIELD_3)
        direction_id = np.frombuffer(direction_id_bytes, dtype=np.int16, count=1)[0]
        direction = ENCODING_TO_DIRECTION[direction_id]

        duration_bytes = get_field(msg, FIELD_2)
        duration = np.frombuffer(duration_bytes, dtype=np.half, count=1)[0]

        altitude_bytes = get_field(msg, FIELD_4)
        altitude = np.frombuffer(altitude_bytes, dtype=np.half, count=1)[0]

        return LinearMovement(self._drone, direction, duration, altitude=altitude)

    def hover_task_decode(self, msg):
        """Decodes data into a Hover task.

        Parameters
        ----------
        msg : str
            The msg to be translated into a task.
        """
        altitude_bytes = get_field(msg, FIELD_3)
        altitude = np.frombuffer(altitude_bytes, dtype=np.half, count=1)[0]

        duration_bytes = get_field(msg, FIELD_2)
        duration = np.frombuffer(duration_bytes, dtype=np.half, count=1)[0]

        return Hover(self._drone, altitude, duration)

# Maps task ID to a function that decodes a binary message for that task
TASK_TO_DECODER = {
    TASK_EXIT:    TaskFactory.exit_task_decode,
    TASK_LAND:    TaskFactory.land_task_decode,
    TASK_TAKEOFF:    TaskFactory.takeoff_task_decode,
    TASK_LINEAR_MOVEMENT:    TaskFactory.linear_movement_task_decode,
    TASK_HOVER:    TaskFactory.hover_task_decode
}
