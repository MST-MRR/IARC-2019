"""Class for decoding array of bytes into keyword dictionary."""

import numpy as np
import sys
import threading
import traceback

from encodings import Encodings
from flight import constants as constants

# Fields starting indeces
FIELDS = [Encodings.FIELD_WIDTH * x for x in range(Encodings.NUM_FIELDS)]

def get_field(msg, field):
    """Returns the bytes associated with given field."""
    return msg[field:field + Encodings.FIELD_WIDTH]

def data_from_bytes(field, msg, data_type):
    """Extracts typed data from a bytearray.

    Paramters
    ---------
    field : int
        The field index to extract data from.
    msg : bytearray
        The array of bytes.
    type
        The data type the bytes should be cast to.
    """
    raw_bytes = get_field(msg, field)
    return np.frombuffer(raw_bytes, dtype=data_type, count=1)[0]

class Decoder:
    """Decodes an array of bytes into a dictionary."""

    SPECIAL_KEYWORDS = {
        'direction': lambda direction_id : Encodings.Directions[direction_id]
    }

    @staticmethod
    def decode(msg):
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
            task_id = data_from_bytes(FIELDS[Encodings.TASK_ID_FIELD], msg, constants.INT)
            priority_id = data_from_bytes(FIELDS[Encodings.PRIORITY_FIELD], msg, constants.INT)

            args = {}

            task = Encodings.Tasks[task_id]
            args['task'] = task

            args['priority'] = Encodings.Priorities[priority_id]

            data_types = Encodings.TypeOrders[task]
            keywords = Encodings.KeywordArguments[task]

            # Using the gathered list of data_type and keywords, parse each
            # field into data, and then store that data in a dictionary
            for index, data_type, keyword in zip(range(Encodings.NUM_FIELDS), data_types, keywords):
                arg = data_from_bytes(FIELDS[index + Encodings.COMMON_FIELDS], msg, data_type)
                # Convert from numpy data type to the native version of that
                # datatype
                arg = Encodings.TypeToNativeType[data_type](arg)
                # Check to see if keyword is "special" (i.e. needs further
                # processing). This will be the case for enum types.
                if keyword in Decoder.SPECIAL_KEYWORDS.keys():
                    arg = Decoder.SPECIAL_KEYWORDS[keyword](arg)
                # Add the argument to the dictionary
                args[keyword] = arg

            return args
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                        limit=2, file=sys.stdout)
