import threading

from ..drone.drone_controller import DroneController
from .. import constants as c
from ... import flightconfig as f

def input_loop(controller):
    """Simple command line interface to drone controller.

    exit: lands and terminates program
    land: land <priority>
    hover: hover <duration> <priority>
    takeoff: takeoff <altitude>
    move: move <FOWARD,BACKWARD,LEFT,RIGHT> <duration> <priority>

    Notes
    -----
    Priority is one of "high", "med", or "low".
    """
    while True:
        command = raw_input('> ').lower()
        commands = command.split()
        if len(commands) == 1 and commands[0] == "exit":
            controller.add_exit_task()
            return
        elif len(commands) == 2 and commands[0] == "land":
            priority = get_priority(commands[1])
            controller.add_land_task(priority)
        elif len(commands) == 3 and commands[0] == "hover":
            priority = get_priority(commands[2])
            controller.add_hover_task(
                f.DEFAULT_ALTITUDE, float(commands[1]), priority)
        elif len(commands) == 2 and commands[0] == "takeoff":
            controller.add_takeoff_task(float(commands[1]))
        elif len(commands) == 4 and commands[0] == "move":
            priority = get_priority(commands[3])
            direction = get_direction(commands[1])

            if priority is None or direction is None:
                print "> Invalid movement command"
                continue
            else:
                controller.add_linear_movement_task(
                    direction, float(commands[2]), priority)
        else:
            print "> Unknown command"

def get_priority(string):
    """Gets priority level from a string."""
    priority = None
    if string == "high":
        priority = c.Priorities.HIGH
    elif string == "med":
        priority = c.Priorities.MEDIUM
    elif string == "low":
        priority = c.Priorities.LOW

    return priority

def get_direction(string):
    """Gets direction from a string."""
    direction = None
    if string == "forward":
        direction = c.Directions.FORWARD
    elif string == "backward":
        direction = c.Directions.BACKWARD
    elif string == "left":
        direction = c.Directions.LEFT
    elif string == "right":
        direction = c.Directions.RIGHT

    return direction

# Make the controller object
controller = DroneController(c.Drones.LEONARDO_SIM)

# Make a thread whose target is a command line interface
input_thread = threading.Thread(target=input_loop, args=(controller,))

input_thread.start()

controller.run()
