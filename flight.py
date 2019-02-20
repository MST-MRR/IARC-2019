"""CLI wrapper for flight, runs flight code using HTTP commands"""
import argparse
import importlib
import json
import logging
import socket
import sys
import threading

import flight.constants as c
import flightconfig as fc
from flight.drone.drone_controller import DroneController

TCP_IP = '192.168.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024


def set_keepalive_linux(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.

    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)


def set_keepalive_osx(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.

    sends a keepalive ping once every 3 seconds (interval_sec)
    """
    # scraped from /usr/include, not exported by python's socket module
    tcp_keepalive = 0x10
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, tcp_keepalive, interval_sec)


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
        return False
    elif command == "land":
        controller.add_land_task(priority)
    elif command == "hover":
        controller.add_hover_task(fc.DEFAULT_ALTITUDE, int(meta["time"]),
                                  priority)
    elif command == "takeoff":
        controller.add_takeoff_task(int(meta["altitude"]))
    elif command == "move":
        controller.add_linear_movement_task(direction, int(meta["time"]),
                                            priority)
    return True


def get_priority(priority):
    return get_enum(c.Priorities, priority)


def get_direction(direction):
    return get_enum(c.Directions, direction)


def get_enum(enum, key):
    item = key.upper()
    if hasattr(enum, item):
        return getattr(enum, item)
    else:
        raise InvalidDirectionException(
            'Expected value for type {}, got {}.'.format(type(enum), item))


def start_ai(controller, routine):
    importlib.import_module("flight.AIs.{}".format(routine))


def kill_ai(controller):
    pass


def list_tasks(controller):
    return controller.queue


def add_task(args, controller, data):
    if args.debug:
        # If in debug mode
        if not ("command" in data and "meta" in data):
            logging.error("command and meta required")
            return True
        command = data["command"].lower()
        meta = data["meta"]
        try:
            return debug_add_task(controller, command, meta)
        except (InvalidDirectionException, InvalidPriorityException) as err:
            return err
        except Exception as err:
            logging.error("Unexpected error, killing drone" + str(err))
            debug_add_task(controller, "exit", {})
            return False
    elif args.routine:
        # If in production mode, starting or stopping drone is only option
        # get push data and check if start or kill
        command = data["command"].lower()
        if command == "start":
            # start routine
            start_ai(controller, args.routine)
        elif command == "kill":
            # force into land
            kill_ai(controller)

        return "routine " + args.routine + " in progress"


def tcp_thread(args, controller):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set_keepalive_osx(s)
    set_keepalive_linux(sock, max_fails=2)
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    print('Connection address:', addr)
    succ = True

    try:
        while succ:
            data = conn.recv(BUFFER_SIZE)
            print("received data:", data)
            if data:
                succ = add_task(args, controller, json.loads(data))
                if succ:
                    conn.send("Success")
            else:
                conn.send("stop")
    except socket.error:
        controller.add_exit_task(c.Priorities.HIGH)
        print("Killing drone because of connection loss")

    conn.send("Killing session")
    logging.info("Ending session")
    conn.close()


def main():
    # Get Command Line Arguments
    args = parse_args()

    # Establish controller
    controller = DroneController(c.Drones.LEONARDO_SIM)
    # Run TCP server on seperate thread
    server_thread = threading.Thread(
        target=tcp_thread, args=(args, controller))
    server_thread.daemon = True

    server_thread.start()
    controller.run()


if __name__ == "__main__":
    main()
