from commands import COMMANDS
from exceptions import BadParams


def parse(message):
    com_type = message[0]
    if com_type in COMMANDS:
        command = COMMANDS[com_type]()

        req_params = command.required_params()
        print(req_params)
        try:
            for index, value in enumerate(message[1:]):
                command.add(req_params[index], int(value))
        except IndexError:
            raise BadParams("Too many elements")

        final = command.get()
        print(final)


if __name__ == "__main__":
    test_bytes = "03"
    test2_bytes = "32F5"

    # linear movement requires 4 args
    fail_bytes = "33"
    # exit requires 2 args
    fail2_bytes = "035968"

    ans = input()
    parse(ans)
    # parse(test_bytes)
    # parse(test2_bytes)
    # parse(fail_bytes)
    # parse(fail2_bytes)
