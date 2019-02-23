"""
Contains the grammar used to specify a new kind of task to be sent over
the network.
"""

from collections import OrderedDict

class BadParams(Exception):
    pass

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
        for value in "values"():
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


COMMANDS = [ExitCommand, LandCommand, TakeoffCommand, LinearMovementCommand,
   HoverCommand]


DIRECTIONS = {
    "UP": '0',
    "DOWN": '1',
    "LEFT": '2',
    "RIGHT": '3',
    "FORWARD": '4',
    "BACKWARD": '5'
}

PRIORITIES = {
    "LOW": '1',
    "MEDIUM": '2',
    "HIGH": '3'
}

HEX = {
    "0": '0',
    "1": '1',
    "2": '2',
    "3": '3',
    "4": '4',
    "5": '5',
    "6": '6',
    "7": '7',
    "8": '8',
    "9": '9',
    "10": 'A',
    "11": 'B',
    "12": 'C',
    "13": 'D',
    "14": 'E',
    "15": 'F'
}

MAPPINGS = {
    "direction": DIRECTIONS,
    "priority": PRIORITIES
}