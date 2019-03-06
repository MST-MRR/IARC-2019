"""Constructs and destructs tasks that the drone controller can perform. The
encoding have been defined in command_encodings.ods (see team drive)."""

import numpy as np

import config
from encodings import Encodings
from flight.tasks import Exit, Land, Takeoff, TakeoffSim, Hover, LinearMovement
import flight.constants as constants

class BadParams(Exception):
    """Thrown when a faulty encoding is encountered."""
    pass

EMPTY = EMPTY_FIELD = np.int16(0).tobytes() # 16 bits, all zero

class TaskEncodings:
    """Tasks mapped to numeric encoding."""
    EXIT = 0
    LAND = 1
    TAKEOFF = 2
    LINEAR_MOVEMENT = 3
    HOVER = 4
    YAW = 5
    CIRCLE = 6
    MOVEMENT = 7

# Map direction encoding to Direction enum
DIRECTION_ENCODINGS = [
    constants.Directions.UP,      # 0
    constants.Directions.DOWN,    # 1
    constants.Directions.LEFT,    # 2
    constants.Directions.RIGHT,   # 3
    constants.Directions.FORWARD, # 4
    constants.Directions.BACKWARD # 5
]

# Map priority encoding to Priority enum
PRIORITY_ENCODINGS = [
    constants.Priorities.LOW,    # 0
    constants.Priorities.MEDIUM, # 1
    constants.Priorities.HIGH    # 2
]

def get_field(msg, field):
    return msg[field:field + FIELD_WIDTH]

class TaskFactory(object):
    """Encodes and decodes tasks.

    Attributes
    ----------
    _drone : flight.drone.Drone
        The drone that tasks are being created for. Only needed if decoding.
    """

    def exit_task_encode(self, priority=constants.Priorities.HIGH):
        """Translates parameters into an encoded exit task.

        Parameters
        ----------
        priority : constants.Priorities
            Priority at which the task should be executed.
        """
        num_empty = 6
        msg = bytearray()
        msg += np.int16(TaskEncodings.EXIT).tobytes() # Task id
        msg += np.int16(PRIORITY_ENCODINGS.index(priority)).tobytes() # Priority
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
        msg += np.int16(TaskEncodings.LAND).tobytes() # Task id
        msg += np.int16(PRIORITY_ENCODINGS.index(priority)).tobytes() # Priority
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
        msg += np.int16(TaskEncodings.TAKEOFF).tobytes() # Task id
        msg += np.int16(PRIORITY_ENCODINGS.index(priority)).tobytes() # Priority
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
        msg += np.int16(TaskEncodings.LINEAR_MOVEMENT).tobytes() # Task id
        msg += np.int16(PRIORITY_ENCODINGS.index(priority)).tobytes() # Priority
        msg += np.half(duration).tobytes() # Duration
        msg += np.int16(DIRECTION_ENCODINGS.index(direction)).tobytes() # Direction
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
        msg += np.int16(TaskEncodings.HOVER).tobytes() # Task id
        msg += np.int16(PRIORITY_ENCODINGS.index(priority)).tobytes() # Priority
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

        Notes
        -----
        This function looks at the first field to determine task type, and then
        calls the appropriate specific decoding function.
        """
        try:
            task_id_bytes = get_field(msg, FIELD_0)
            task_id= np.frombuffer(task_id_bytes, dtype=np.int16, count=1)[0] # returns array, take first and only element
            if task_id in TASK_TO_DECODER.keys():
                priority_id_bytes = get_field(msg, FIELD_1)
                priority_id = np.frombuffer(priority_id_bytes, dtype=np.int16, count=1)[0]
                priority = PRIORITY_ENCODINGS[priority_id]
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
        return Exit()


    def land_task_decode(self, msg):
        """Decodes data into a Land task.

        Parameters
        ----------
        msg : str
            The msg to be translated into a task.
        """
        return Land()


    def takeoff_task_decode(self, msg):
        """Decodes data into a Takeoff task.

        Parameters
        ----------
        msg : str
            The msg to be translated into a task.
        """
        altitude_bytes = get_field(msg, FIELD_2)
        altitude = np.frombuffer(altitude_bytes, dtype=np.half, count=1)[0]

        if config.IS_SIMULATION:
            task = TakeoffSim(altitude)
        else:
            task = Takeoff(altitude)
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
        direction = DIRECTION_ENCODINGS[direction_id]

        duration_bytes = get_field(msg, FIELD_2)
        duration = np.frombuffer(duration_bytes, dtype=np.half, count=1)[0]

        altitude_bytes = get_field(msg, FIELD_4)
        altitude = np.frombuffer(altitude_bytes, dtype=np.half, count=1)[0]

        return LinearMovement(direction, duration, altitude=altitude)


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

        return Hover(altitude, duration)


# NOTE: this has to be at bottom or else python doesn't know about the TaskFactory
# methods, and so raises an error. Is there a way around this?
# Maps task ID to a function that decodes a binary message for that task
TASK_TO_DECODER = {
    TaskEncodings.EXIT:             TaskFactory.exit_task_decode,
    TaskEncodings.LAND:             TaskFactory.land_task_decode,
    TaskEncodings.TAKEOFF:          TaskFactory.takeoff_task_decode,
    TaskEncodings.LINEAR_MOVEMENT:  TaskFactory.linear_movement_task_decode,
    TaskEncodings.HOVER:            TaskFactory.hover_task_decode
}
