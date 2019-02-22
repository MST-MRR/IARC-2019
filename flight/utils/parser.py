from commands import COMMANDS

test_bytes = "03"
test2_bytes = "32F5"

fail_bytes = "33"


def parse(message):
    com_type = message[0]
    print(com_type)
    if com_type in COMMANDS:
        command = COMMANDS[com_type]
        for index, param in enumerate(command.required_params(command)):
            command.add(command, param, message[1:][index])
        final = command.get(command)
        print(final)
    else:
        print("AHH")


if __name__ == "__main__":
    print(COMMANDS)
    parse(fail_bytes)
    parse(test_bytes)
    parse(test2_bytes)
