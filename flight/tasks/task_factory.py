"""Class that takes a dictionary and turns it into a fully configured class."""

import numpy as np

import config
from encodings import Encodings
import flight.constants as constants
from flight.tasks import Tasks

class TaskFactory:
    """Turns a dictionary into a fully configured task."""

    TASK_TYPE_LOOKPUP = {
        Encodings.Tasks.EXIT:           Tasks.Exit,
        Encodings.Tasks.LAND:           Tasks.Land,
        Encodings.Tasks.TAKEOFF:        Tasks.Takeoff,
        Encodings.Tasks.LINEAR_MOVE:    Tasks.LinearMovement,
        Encodings.Tasks.HOVER:          Tasks.Hover
    }

    CLI_STR_TO_TASK = {
        Encodings.CommandLine.EXIT:         Encodings.Tasks.EXIT,
        Encodings.CommandLine.LAND:         Encodings.Tasks.LAND,
        Encodings.CommandLine.TAKEOFF:      Encodings.Tasks.TAKEOFF,
        Encodings.CommandLine.LINEAR_MOVE:  Encodings.Tasks.LINEAR_MOVE,
        Encodings.CommandLine.HOVER:        Encodings.Tasks.HOVER
    }

    @staticmethod
    def from_args(**kwargs):
        """Converts a dictionary of keywords and arguments to a fully
        configured task.

        Parameters
        ----------
        kwargs : dict
            The following arguments are required:
                task : Encodings.CommandLine or Encodings.Tasks
                priority: constants.Priorities
            Based on choice of task, a particular set of arguments will be
            required. The keyword/arguments are the exact parameter names
            for the task being constructed.
        """
        task = kwargs[Encodings.TASK_KEYWORD]

        # The task argument must be a strin
        if task in Encodings.CommandLine:
            task = TaskFactory.CLI_STR_TO_TASK[task]
        elif task not in Encodings.Tasks:
            raise ValueError

        task = TaskFactory.TASK_TYPE_LOOKPUP[task]

        if task is Tasks.Takeoff and config.IS_SIMULATION:
            task = Tasks.TakeoffSim

        priority = kwargs[Encodings.PRIORITY_KEYWORD]

        del kwargs[Encodings.TASK_KEYWORD]
        del kwargs[Encodings.PRIORITY_KEYWORD]

        return (priority, task(**kwargs))
