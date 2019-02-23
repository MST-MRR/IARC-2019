"""
Contains the grammar used to specify a new kind of task to be sent over
the network.
"""

from collections import OrderedDict
from flight import constants as c
from flight.utils.exceptions import BadParams


class Command:
    """

        Generic class for parsing and checking correctness of commands

    """
    _name = None
    _param_list = None

    def __init__(self):
        self._params = OrderedDict(
            [(param, None) for param in self._param_list])

    def add(self, param, value):
        """Tries to insert value into specific parameter field"""
        try:
            self._params[param] = value
        except IndexError:
            raise BadParams("Parameter doesn't exist for {}".format(self._name))

    def get(self):
        """

        Tries to get completed command object, is validated before return

        Returns
        -------
        OrderedDict
            Contains all parameters and their corresponding values

        """
        for value in self._params.values():
            if value is None:
                raise BadParams(
                    "Not enough Parameters for {}".format(self._name))
        return self._params

    @property
    def name(self):
        return self._name

    @property
    def required_params(self):
        """List of required parameters"""
        return self._param_list


class ExitCommand(Command):
    """The command associated with the Exit task"""
    _name = "EXIT"
    _param_list = ["priority"]


class LandCommand(Command):
    """The command associated with the Land task"""
    _name = "LAND"
    _param_list = ["priority"]


class TakeoffCommand(Command):
    """The command associated with the Takeoff task"""
    _name = "TAKEOFF"
    _param_list = ["priority", "altitude"]


class LinearMovementCommand(Command):
    """The command associated with the LinearMovement task"""
    _name = "LINEAR_MOVEMENT"
    _param_list = ["priority", "duration", "direction"]


class HoverCommand(Command):
    """The command associated with the Hover task"""
    _name = "HOVER"
    _param_list = ["priority", "duration", "altitude"]


DIRECTIONS = {
    "0": "UP",
    "1": "DOWN",
    "2": "LEFT",
    "3": "RIGHT",
    "4": "FORWARD",
    "5": "BACKWARD"
}

PRIORITIES = {
    "1": "HIGH",
    "2": "MEDIUM",
    "3": "LOW"
}

COMMANDS = {
    "0": ExitCommand,
    "1": LandCommand,
    "2": TakeoffCommand,
    "3": LinearMovementCommand,
    "4": HoverCommand
}
