"""
Takes a given message and attempts to parse out the parameters and
commands
"""
from flight.utils.commands import COMMANDS, DIRECTIONS, PRIORITIES
from flight.utils.exceptions import BadParams


def parse_message2(message):
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

        req_params = command.required_params
        print(req_params)
        try:
            for index, value in enumerate(message[1:]):
                print(req_params[index])
                if req_params[index] == "priority":
                    print(PRIORITIES[value])
                    command.add(req_params[index], PRIORITIES[value])
                elif req_params[index] == "direction":
                    command.add(req_params[index], DIRECTIONS[value])
                else:
                    command.add(req_params[index], int(value))
        except IndexError:
            raise BadParams("Too many elements")

        return dict(meta=dict(command.get()), command=command.name)
    else:
        return False
