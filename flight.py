"""CLI wrapper for flight, runs flight code using HTTP commands"""
import argparse
import logging
import sys
import threading

from flask import Blueprint, Flask, jsonify, request

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
    commands = Blueprint('commands', __name__, url_prefix='/commands')

    @commands.route('/', methods=["GET"])
    def list_tasks():
        return jsonify(controller.queue), 200

    @commands.route('/', methods=["POST"])
    def push_command():
        data = request.get_json()

        if args.debug:
            # If in debug mode
            if not ("command" in data and "meta" in data):
                return "command and meta required", 400
            command = data["command"].lower()
            meta = data["meta"]
            try:
                debug_add_task(controller, command, meta)
                return "success", 200
            except (InvalidDirectionException,
                    InvalidPriorityException) as err:
                return jsonify(err), 400
            except Exception as err:
                logging.error("Unexpected error, killing drone")
                debug_add_task(controller, "exit", {})
                return "Unexpected error, killing drone " + str(err), 400
        elif args.routine:
            # If in production mode, starting or stopping drone is only option
            # get push data and check if start or kill
            # if command == "start":
            #     start routine
            # elif command == "kill":
            #     force into land

            return "routine " + args.routine + " in progress", 200

    return [commands]


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


def flask_thread(args, controller):
    blueprints = create_routes(args, controller)
    app = Flask(__name__)
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    app.run("127.0.0.1", 8000)


def main():
    # Get Command Line Arguments
    args = parse_args()

    # Establish controller
    controller = DroneController(c.Drones.LEONARDO_SIM)
    # Run Flask server on seperate thread
    server_thread = threading.Thread(
        target=flask_thread, args=(args, controller))
    server_thread.daemon = True

    server_thread.start()
    controller.run()

    # After controller has stopped, exit Flask server.
    sys.exit(0)


if __name__ == "__main__":
    main()
