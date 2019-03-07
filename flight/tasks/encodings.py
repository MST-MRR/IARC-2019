"""A class used for encoding/decoding lookups."""

import numpy as np

from flight import constants as constants
from flight.tasks import *
from flight.utils.bidirectional_dictionary import BidirectionalDictionary

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

    # Maps a task type to its ID (its index in the list)
    Tasks = BidirectionalDictionary([
        Exit,               # 0
        Land,               # 1
        Takeoff,            # 2
        LinearMovement,     # 3
        Hover               # 4
        # TODO: add Yaw, Circle, Movement
    ])

    # Maps a Direction enum type to its ID (its index in the list)
    Directions = BidirectionalDictionary([
        constants.Directions.UP,      # 0
        constants.Directions.DOWN,    # 1
        constants.Directions.LEFT,    # 2
        constants.Directions.RIGHT,   # 3
        constants.Directions.FORWARD, # 4
        constants.Directions.BACKWARD # 5
    ])

    # Maps a Priorities enum type to its ID (its index in the list)
    Priorities = BidirectionalDictionary([
        constants.Priorities.LOW,    # 0
        constants.Priorities.MEDIUM, # 1
        constants.Priorities.HIGH    # 2
    ])

    # The ordering of types defined for each task (includes all fields after
    # type_id and priority)
    TypeOrders =  {
        Exit: [],

        Land: [],

        Takeoff: [constants.FLOAT],

        LinearMovement: [constants.FLOAT, constants.INT, constants.FLOAT],

        Hover: [constants.FLOAT, constants.FLOAT]
    }

    # Keyword shared across all tasks for task type
    TASK_KEYWORD = 'task'

    # Keyword shared across all tasks for priority
    PRIORITY_KEYWORD = 'priority'

    # The keyword arguments that a task expected upon its __init__ function
    # being called
    KeywordArguments = {
        Exit: [],

        Land: [],

        Takeoff: ['altitude'],

        LinearMovement: ['duration', 'direction', 'altitude'],

        Hover: ['duration', 'altitude']
    }

    # Maps type used for encoding to the native version of the type for the
    # system the code is running on
    TypeToNativeType = {
        constants.FLOAT: float,
        constants.INT: int
    }
