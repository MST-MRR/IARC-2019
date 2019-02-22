from exceptions import BadParams
from collections import OrderedDict


class Command:
    _name = None
    _param_list = None

    def __init__(self):
        self._params = OrderedDict(
            [(param, None) for param in self._param_list])

    def add(self, param, value):
        try:
            self._params[param] = value
        except IndexError:
            raise BadParams("Parameter doesn't exist for {}".format(self._name))

    def get(self):
        for value in self._params.values():
            if value is None:
                raise BadParams(
                    "Not enough Parameters for {}".format(self._name))
        return self._params

    def required_params(self):
        return self._param_list


class ExitCommand(Command):
    _name = "EXIT"
    _param_list = ["priority"]


class LandCommand(Command):
    _name = "LAND"
    _param_list = ["priority"]


class TakeoffCommand(Command):
    _name = "TAKEOFF"
    _param_list = ["priority", "altitude"]


class LinearMovementCommand(Command):
    _name = "LINEAR_MOVEMENT"
    _param_list = ["priority", "duration", "direction"]


class HoverCommand(Command):
    _name = "HOVER"
    _param_list = ["priority", "duration", "altitude"]


COMMANDS = {
    "0": ExitCommand,
    "1": LandCommand,
    "2": TakeoffCommand,
    "3": LinearMovementCommand,
    "4": HoverCommand
}
