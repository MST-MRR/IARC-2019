class ExitCommand:
    priority = 1

class LinearMovementCommand:
    priority = 1
    duration = 2
    direction = 3

commands = {
    b"0": ExitCommand,
    b"3": LinearMovementCommand
}


