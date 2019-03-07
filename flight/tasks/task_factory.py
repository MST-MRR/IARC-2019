"""Class that takes a dictionary and turns it into a fully configured class."""

import numpy as np

import config
from encodings import Encodings
import flight.constants as constants

class TaskFactory:
    """Turns a dictionary into a fully configured task."""

    @staticmethod
    def from_dict(**kwargs):
        task = kwargs['task']
        priority = kwargs['priority']

        del kwargs['task']
        del kwargs['priority']

        return (priority, task(**kwargs))
