"""A class used for encoding/decoding lookups."""

from enum import Enum
import numpy as np

from flight import constants as constants
from flight.tasks import Tasks as task
from flight.utils.bidirectional_dictionary import BidirectionalDictionary

class TaskInfo:
    """Contains the name, ordering of types, and keywords for a task."""
    def __init__(self, type_order, keywords):
        """Initialize the information for this kind of task.

        Parameters
        ----------
        type_order : list[type]
            A list of the expected types for an encoded/decoded message, in
            order.
        keywords : list[str]
            A list of the keyword arguments associated with initializing this
            kind of task.
        """
        self.type_order = type_order
        self.keywords = keywords

class Encodings:
    """Contains encodings defined in https://docs.google.com/spreadsheets/u/1/d/1evjB_2ChFrgppTaEZ03ktKQYPjTJT50ZoAbLgZen3No/edit?usp=drive_web&ouid=112691440415013941668."""

    # The number of fields in an encoded task
    NUM_FIELDS = 8

    # The number of fields shared by all tasks (task_id and priority)
    COMMON_FIELDS = 2

    # The width in bytes of each field
    FIELD_WIDTH = 4

    # Index of the type id field
    TASK_ID_FIELD = 0

    # Index of the priority field
    PRIORITY_FIELD = 1

    # Keyword shared across all tasks for task type
    TASK_KEYWORD = 'task'

    # Keyword shared across all tasks for priority
    PRIORITY_KEYWORD = 'priority'

    class CommandLine(Enum):
        """The command-line string name for each task."""
        EXIT = 'exit'

        LAND = 'land'

        TAKEOFF = 'takeoff'

        LINEAR_MOVE = 'move'

        HOVER = 'hover'

    class Tasks(Enum):
        """The ID of each task."""
        EXIT = 0

        LAND = 1

        TAKEOFF = 2

        LINEAR_MOVE = 3

        HOVER = 4

    # Maps task id to information about the task
    INFO = [
        TaskInfo([], []),       # 0 Exit

        TaskInfo([], []),       # 1 Land

        TaskInfo(               # 2 Takeoff
            [constants.FLOAT],
            ['altitude']),

        TaskInfo(               # 3 Linear Movement
            [constants.FLOAT, constants.INT, constants.FLOAT],
            ['duration', 'direction', 'altitude']),

        TaskInfo(               # 4 Hover
            ['duration', 'altitude'],
            ['duration', 'altitude'])
    ]

    # Maps a Direction enum type to its ID (its index in the list)
    DIRECTIONS = BidirectionalDictionary([
        constants.Directions.UP,      # 0
        constants.Directions.DOWN,    # 1
        constants.Directions.LEFT,    # 2
        constants.Directions.RIGHT,   # 3
        constants.Directions.FORWARD, # 4
        constants.Directions.BACKWARD # 5
    ])

    # Maps a Priorities enum type to its ID (its index in the list)
    PRIORITIES = BidirectionalDictionary([
        constants.Priorities.LOW,    # 0
        constants.Priorities.MEDIUM, # 1
        constants.Priorities.HIGH    # 2
    ])

    # Maps type used for encoding to the native version of the type for the
    # system the code is running on
    TO_NATIVE_TYPE = {
        constants.FLOAT: float,
        constants.INT: int
    }
