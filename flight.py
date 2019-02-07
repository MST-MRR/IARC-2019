import argparse
import logging
import sys
import threading

from flask import Blueprint, Flask, jsonify, request

import flight.constants as c
import flightconfig as fc
from flight.drone.drone_controller import DroneController


class InvalidDirectionException(Exception):
    pass


class InvalidPriorityException(Exception):
    pass


parser = argparse.ArgumentParser(
    description='MRRDT flight command line interface. Used to fly the drone.')
parser.add_argument('-d', '--debug', action="store_true")
parser.add_argument('routine', nargs="?", default="stall", type=str)

args = parser.parse_args()

if not args.debug and not args.routine:
    logging.error("Please specify routine.")
    sys.exit(1)

controller = DroneController(c.Drones.LEONARDO_SIM)
controller.add_takeoff_task(fc.DEFAULT_ALTITUDE)

app = Flask(__name__)

commands = Blueprint('commands', __name__, url_prefix='/commands')


@commands.route('/', methods=["GET"])
def list_tasks():
    return jsonify(controller.queue), 200


@commands.route('/', methods=["POST"])
def push_command():
    data = request.get_json()
    #if args.debug:
    if not ("command" in data and "meta" in data):
        return "command and meta required", 400
    command = data["command"].lower()
    meta = data["meta"]
    try:
        debug_add_task(command, meta)
        return "success", 200
    except InvalidDirectionException as e:
        return jsonify(e), 400
    except InvalidPriorityException as e:
        return jsonify(e), 400
    except:
        logging.error("Unexpected error, killing drone")
        debug_add_task("exit", {})
        sys.exit(1)
    #elif args.routine:
        # get push data and check if start or kill
        # if command == "start":
        #     start routine
        # elif command == "kill":
        #     force into land
        #return "routine " + args.routine + " in progress", 200


def debug_add_task(command, meta):
    if "priority" in meta:
        priority = get_priority(meta["priority"])
    if "direction" in meta:
        direction = get_direction(meta["direction"])

    if command == "exit":
        controller.add_land_task(c.Priorities.HIGH)
    elif command == "land":
        controller.add_land_task(priority)
    elif command == "hover":
        controller.add_hover_task(fc.DEFAULT_ALTITUDE, meta["time"], priority)
    elif command == "takeoff":
        controller.add_takeoff_task(meta["altitude"])
    elif command == "move":
        controller.add_linear_movement_task(direction, meta["time"], priority)


def get_priority(priority):
    if priority == "high":
        return c.Priorities.HIGH
    elif priority == "med":
        return c.Priorities.MEDIUM
    elif priority == "low":
        return c.Priorities.LOW
    else:
        raise InvalidPriorityException


def get_direction(direction):
    if direction == "forward":
        return c.Directions.FORWARD
    if direction == "back":
        return c.Directions.BACKWARD
    if direction == "left":
        return c.Directions.LEFT
    if direction == "right":
        return c.Directions.RIGHT
    else:
        raise InvalidDirectionException


def flask_thread():
    app.register_blueprint(commands)
    app.run("127.0.0.1", 8000)


def main():
    server_thread = threading.Thread(target=flask_thread)
    server_thread.start()
    controller.run()

if __name__ == "__main__":
    main()
