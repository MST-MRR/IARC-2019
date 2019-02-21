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


class BadParams(Exception):
    """Thrown when parameters are incorrect for task"""

    def __str__(self):
        return str(self)


def parse_args():
    """

    Take in Command Line Arguments and give back args to program.

    Returns
    -------
    argparse.Namespace
        Arguments assembled by argparse.

    """
    parser = argparse.ArgumentParser(
        description='MRRDT flight command line interface.')
    parser.add_argument('-d', '--debug', action="store_true")
    parser.add_argument('routine', nargs="?", default="", type=str)

    args = parser.parse_args()

    if not args.debug and not args.routine:
        logging.error("Please specify routine.")
        sys.exit(1)
    return args


def debug_add_task(controller, command, meta):
    """

    Gives command to drone controller in the case of debug flight

    Parameters
    ----------
    controller : flight.drone.drone_controller.DroneController
        Drone controller object used for handling tasks
    command : str
        Command name
    meta : dict
        Contains other information needed to perform specified command

    Returns
    -------
    bool
        Should the program continue?

    """

    if command == "exit":
        controller.add_exit_task(c.Priorities.HIGH)
        return False
    elif command == "takeoff":
        if "altitude" in meta:
            controller.add_takeoff_task(int(meta["altitude"]))
        else:
            raise BadParams("altitude not specified")
    elif command == "land":
        if "priority" in meta:
            priority = get_enum(c.Priorities, meta["priority"])
            controller.add_land_task(priority)
        else:
            raise BadParams("priority not specified")
    elif command == "hover":
        if "priority" in meta:
            priority = get_enum(c.Priorities, meta["priority"])
            controller.add_hover_task(fc.DEFAULT_ALTITUDE, int(meta["time"]),
                                      priority)
        else:
            raise BadParams("priority not specified")
    elif command == "move":
        if "priority" in meta and "direction" in meta:
            priority = get_enum(c.Priorities, meta["priority"])
            direction = get_enum(c.Directions, meta["direction"])
            controller.add_linear_movement_task(direction, int(meta["time"]),
                                                priority)
        else:
            raise BadParams("priority or direction not specified")
    return True


def get_enum(enum, key):
    """

    Retrieves key from enum if it exists

    Parameters
    ----------
    enum : enum.Enum
        The enum that is being searched
    key : str
        The key that is supposed to exist in the enum

    Returns
    -------
    any
        Value of enum from corresponding key

    """
    item = key.upper()
    if hasattr(enum, item):
        return getattr(enum, item)
    else:
        raise BadParams(
            'Expected value for type {}, got {}.'.format(type(enum), item))


def start_ai(routine):
    """

    Starts the specified AI

    Parameters
    ----------
    routine : str
        Name of the routine being asked to run

    """
    # TODO grab ai class and run it
    importlib.import_module("flight.AIs.{}".format(routine))


def kill_ai(controller):
    """

    Kills the AI being run and subsequently, the drone

    Parameters
    ----------
    controller : flight.drone.drone_controller.DroneController
        Drone controller object used for handling tasks

    """
    controller.add_exit_task(c.Priorities.HIGH)


def close_server(connection):
    """

    Kills the AI being run and subsequently, the drone

    Parameters
    ----------
    connection : socket.socket
        Server socket object

    """
    connection.send("Killing session")
    connection.close()


def parse_message(args, controller, message):
    """

    Takes message and decides how to execute it

    Parameters
    ----------
    args : argparse.Namespace
        Arguments assembled by argparse.
    controller : flight.drone.drone_controller.DroneController
        Drone controller object used for handling tasks
    message : str
        Data for the task in json

    """
    data = json.loads(message)
    if args.debug and "command" in data and "meta" in data:
        # If in debug mode
        if not debug_add_task(controller, data["command"], data["meta"]):
            return False
    elif args.routine and "command" in data:
        # If in production mode, starting or stopping drone is only option
        command = data["command"]
        if command == "start":
            start_ai(args.routine)
        elif command == "kill":
            kill_ai(controller)
        else:
            raise BadParams(
                "Commands for production are either \"start\" or \"kill\"")
    elif args.debug:
        logging.error("command and meta required in debug mode")
    elif args.routine:
        logging.error("command required in production mode")

    return True


def tcp_thread(args, controller):
    """

    Starts the tcp server

    Parameters
    ----------
    args : argparse.Namespace
        Arguments assembled by argparse.
    controller : flight.drone.drone_controller.DroneController
        Drone controller object used for handling tasks

    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    set_keepalive_linux(sock, max_fails=2)
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    print('Connection address:', addr)

    try:
        while True:
            # Get data from TCP connection
            message = conn.recv(BUFFER_SIZE)
            print("received data:", message)

            if message:
                # if not empty
                try:
                    if parse_message(args, controller, message):
                        conn.send("Success")
                    else:
                        close_server(conn)
                        return
                except BadParams as err:
                    logging.error(err)
            else:
                logging.warning("Received empty message")
                conn.send("stop")
    except socket.error:
        logging.error("Killing drone because of connection loss")
    except Exception as err:
        logging.error("Unexpected error, killing drone" + str(err))
    finally:
        logging.info("Ending session")

        kill_ai(controller)
        close_server(conn)


def main():
    """
    Runs the flight code
    """
    # Get Command Line Arguments
    args = parse_args()

    # Establish controller
    controller = DroneController(c.Drones.LEONARDO_SIM)
    # Run TCP server on separate thread
    server_thread = threading.Thread(
        target=tcp_thread, args=(args, controller))
    server_thread.daemon = True

    server_thread.start()
    controller.run()
    server_thread.join()


if __name__ == "__main__":
    main()
