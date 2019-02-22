"""
Takes a given message and attempts to parse out the parameters and
commands
"""
from flight.utils.commands import COMMANDS
from flight.utils.exceptions import BadParams


def parse_message(message):
    """

    Strips message into pieces and uses those pieces to arrange a command

    Parameters
    ----------
    message : str
        the encoded message

    Returns
    -------
    OrderedDict or False
        if it succeeds it will return the command, or it will return False
    """
    com_type = message[0]
    if com_type in COMMANDS:
        command = COMMANDS[com_type]()

        req_params = command.required_params()
        try:
            for index, value in enumerate(message[1:]):
                command.add(req_params[index], value)
        except IndexError:
            raise BadParams("Too many elements")

        return command.get()
    else:
        return False
