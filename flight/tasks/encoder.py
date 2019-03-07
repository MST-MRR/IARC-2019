"""Class for encoding tasks into an array of bytes."""

import numpy as np
import sys
import threading
import traceback

from encodings import Encodings
from flight import constants as constants

# An empty field
EMPTY = EMPTY_FIELD = constants.INT(0).tobytes() # 32 bits, all zero

class Encoder:
    """Encodes a task into a byte array from a dictionary of keyword arguments."""

    # Maps types that must be converted to a function that does the conversion
    SPECIAL_TYPES = {
        constants.Directions: lambda direction : constants.INT(Encodings.Directions[direction]),
        constants.Priorities: lambda priority : constants.INT(Encodings.Priorities[priority])
    }

    @staticmethod
    def encode(**kwargs):
        """Encodes a set up keyword arguments into an array of bytes which
        represent a task.

        Paramters
        ---------
        kwargs : dict
            Always requires the key pairs {task : Encodings.Tasks},
            {priority : flight.constants.Priorites} and the exact keywords that
            are in each of the task initialization functions.
        """
        try:
            task_info = Encodings.Info[kwargs[Encodings.TASK_KEYWORD].value]

            type_order = task_info.type_order
            keywords = task_info.keywords

            msg = bytearray()
            msg += constants.INT(kwargs[Encodings.TASK_KEYWORD].value).tobytes()
            msg += constants.INT(Encodings.Priorities[kwargs[Encodings.PRIORITY_KEYWORD]]).tobytes()

            for data_type, keyword in zip(type_order, keywords):
                if keyword not in kwargs.keys():
                    raise ValueError
                arg = kwargs[keyword]

                # Check to see if this type needs further processing
                # (this will be the case for enum types)
                arg_type = type(arg)
                if arg_type in Encoder.SPECIAL_TYPES.keys():
                    arg = Encoder.SPECIAL_TYPES[arg_type](arg)

                # append the encoded value to the array of bytes
                msg += data_type(arg).tobytes()

            # Pad the rest of the message with empty fields
            for _ in range(Encodings.NUM_FIELDS - len(type_order) - Encodings.COMMON_FIELDS):
                msg += EMPTY_FIELD

            return msg
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                        limit=2, file=sys.stdout)
