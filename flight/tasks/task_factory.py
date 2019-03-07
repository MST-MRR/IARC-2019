"""Class that takes a dictionary and turns it into a fully configured class."""

import numpy as np

import config
from encodings import Encodings
import flight.constants as constants
from flight.tasks import Tasks

class TaskFactory:
    """Turns a dictionary into a fully configured task."""

    TaskTypeLookup = {
        Encodings.Tasks.EXIT:   Tasks.Exit,
        Encodings.Tasks.LAND:   Tasks.Land,
        Encodings.Tasks.TAKEOFF:   Tasks.Takeoff,
        Encodings.Tasks.LINEAR_MOVE:   Tasks.LinearMovement,
        Encodings.Tasks.HOVER:   Tasks.Hover
    }

    @staticmethod
    def from_args(**kwargs):
        task_enum = kwargs[Encodings.TASK_KEYWORD]
        task = TaskFactory.TaskTypeLookup[task_enum]

        if task is Tasks.Takeoff and config.IS_SIMULATION:
            task = Tasks.TakeoffSim

        priority = kwargs[Encodings.PRIORITY_KEYWORD]

        del kwargs['task']
        del kwargs['priority']

        return (priority, task(**kwargs))
