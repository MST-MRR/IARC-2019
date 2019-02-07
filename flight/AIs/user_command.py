import threading

from ..drone.drone_controller import DroneController
from .. import constants as c
from ... import flightconfig as f

def input_loop(controller):
    """Simple command line interface to drone controller.

    exit: lands and terminates program
    land: land <priority>
    hover: hover <duration> <priority>
    takeoff: currently not used for safety reasons
    move: move <FOWARD,BACK,LEFT,RIGHT> <duration> <priority>

    Notes
    -----
    Priority is one of "high", "med", or "low".
    """
    while True:
        command = raw_input('> ')
        command = command.lower()
        commands = command.split()
        if len(commands) == 1 and commands[0] == "exit":
            controller.add_land_task(c.Priorities.HIGH)
            return
        elif len(commands) == 2 and commands[0] == "land":
            priority = get_priority(commands[1])
            controller.add_land_task(priority)
            return
        elif len(commands) == 3 and commands[0] == "hover":
            priority = get_priority(commands[2])
            controller.add_hover_task(
                f.DEFAULT_ALTITUDE, float(commands[1]), priority)
        elif len(commands) == 2 and commands[0] == "takeoff":
            controller.add_takeoff_task(float(commands[1]))
        elif len(commands) == 4 and commands[0] == "move":
            priority = get_priority(commands[3])
            if commands[1] == "forward":
                dir = c.Directions.FORWARD
            elif commands[1] == "backward":
                dir = c.Directions.BACKWARD
            elif commands[1] == "left":
                dir = c.Directions.LEFT
            elif commands[1] == "right":
                dir = c.Directions.RIGHT
            else:
                print "> Invalid movement command"
                continue
            controller.add_linear_movement_task(
                dir, float(commands[2]), priority)
        else:
            print "> Unknown command"

def get_priority(string):
    """Gets priority level from string."""
    if string == "high":
        return c.Priorities.HIGH
    elif string == "med":
        return c.Priorities.MEDIUM
    elif string == "low":
        return c.Priorities.LOW
    else:
        return None

# Make the controller object
controller = DroneController(c.Drones.LEONARDO_SIM)
# Add takeoff task here for now; safety concern otherwise!
controller.add_takeoff_task(f.DEFAULT_ALTITUDE)

# Make a thread whose target is a command line interface
input_thread = threading.Thread(target=input_loop, args=(controller,))

input_thread.start()

controller.run()
