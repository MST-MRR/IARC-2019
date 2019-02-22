from exceptions import BadParams


class Command:
    _name = None
    _params = None

    def add(self, param, value):
        try:
            self._params[param] = value
        except IndexError:
            raise BadParams("Incorrect Parameters for", self._name)

    def get(self):
        for value in self._params.values():
            if value is None:
                raise BadParams("Incorrect Parameters for", self._name)
        else:
            return self._params

    def required_params(self):
        return self._params.values()


class ExitCommand(Command):
    _name = "EXIT"
    _params = {
        "priority": None
    }


class LinearMovementCommand(Command):
    _name = "LINEAR_MOVEMENT"
    _params = {
        "priority": None,
        "duration": None,
        "direction": None
    }


COMMANDS = {
    "0": ExitCommand,
    "3": LinearMovementCommand
}
