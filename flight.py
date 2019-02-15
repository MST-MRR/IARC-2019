"""CLI wrapper for flight, runs flight code using HTTP commands"""
import argparse
import importlib
import logging
import socket
import sys
import threading

import flight.constants as c
import flightconfig as fc
from flight.drone.drone_controller import DroneController


class InvalidDirectionException(Exception):
    """Thrown when specified direction is invalid"""
    pass


class InvalidPriorityException(Exception):
    """Thrown when specified priority is invalid"""
    pass


def parse_args():
    """

    Take in Command Line Arguments and give back args to program.

    Returns
    -------
    argparse.Namespace
        Arguments assembled by argparse.

    """
    parser = argparse.ArgumentParser(
        description=
        'MRRDT flight command line interface. Used to fly the drone.')
    parser.add_argument('-d', '--debug', action="store_true")
    parser.add_argument('routine', nargs="?", default=None, type=str)

    args = parser.parse_args()

    if not args.debug and not args.routine:
        logging.error("Please specify routine.")
        sys.exit(1)
    return args


def create_routes(args, controller):
    """

    Constructs all routes necessary for network flight

    Parameters
    ----------
    args : argparse.Namespace
        Arguments assembled by argparse.
    controller : flight.drone.drone_controller.DroneController
        The second parameter.

    Returns
    -------
    list
        Blueprints to be added to Flask app

    """
    pass


def debug_add_task(controller, command, meta):
    if "priority" in meta:
        priority = get_priority(meta["priority"])
    if "direction" in meta:
        direction = get_direction(meta["direction"])

    if command == "exit":
        controller.add_exit_task(c.Priorities.HIGH)
    elif command == "land":
        controller.add_land_task(priority)
    elif command == "hover":
        controller.add_hover_task(fc.DEFAULT_ALTITUDE, meta["time"], priority)
    elif command == "takeoff":
        controller.add_takeoff_task(meta["altitude"])
    elif command == "move":
        controller.add_linear_movement_task(direction, meta["time"], priority)


def get_priority(priority):
    key = priority.upper()
    if hasattr(c.Priorities, key):
        return getattr(c.Priorities, key)
    else:
        raise InvalidPriorityException(
            'Expected value for type {}, got {}.'.format(
                type(c.Priorities), priority))


def get_direction(direction):
    key = direction.upper()
    if hasattr(c.Directions, key):
        return getattr(c.Directions, key)
    else:
        raise InvalidDirectionException(
            'Expected value for type {}, got {}.'.format(
                type(c.Directions), direction))


def start_ai(routine):
    importlib.import_module("flight.AIs.{}".format(routine))


def kill_ai():
    pass


def list_tasks(controller):
    return controller.queue


def add_task(args, controller, data):
    if args.debug:
        # If in debug mode
        if not ("command" in data and "meta" in data):
            return "command and meta required"
        command = data["command"].lower()
        meta = data["meta"]
        try:
            debug_add_task(controller, command, meta)
            return "success"
        except (InvalidDirectionException, InvalidPriorityException) as err:
            return err
        except Exception as err:
            logging.error("Unexpected error, killing drone")
            debug_add_task(controller, "exit", {})
            return "Unexpected error, killing drone " + str(err)
    elif args.routine:
        # If in production mode, starting or stopping drone is only option
        # get push data and check if start or kill
        command = data["command"].lower()
        if command == "start":
            # start routine
            start_ai(args.routine)
        elif command == "kill":
            # force into land
            kill_ai()

        return "routine " + args.routine + " in progress"


def tcp_thread(args, controller):
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5005
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print('Connection address:', addr)
    while True:
        data = conn.recv(BUFFER_SIZE)
        print("received data:", data)
        conn.send(data)  # echo
    conn.close()
    # kill DroneController


def main():
    # Get Command Line Arguments
    args = parse_args()

    controller = None
    # Establish controller
    # controller = DroneController(c.Drones.LEONARDO_SIM)
    # Run Flask server on seperate thread
    server_thread = threading.Thread(
        target=tcp_thread, args=(args, controller))
    server_thread.daemon = True

    server_thread.start()
    # controller.run()

    # After controller has stopped, exit Flask server.
    sys.exit(0)


if __name__ == "__main__":
    main()
