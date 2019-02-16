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

# from flight.drone.drone_controller import DroneController


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
    TCP_KEEPALIVE = 0x10
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, TCP_KEEPALIVE, interval_sec)


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
        controller.add_hover_task(fc.DEFAULT_ALTITUDE, meta["time"], priority)
    elif command == "takeoff":
        controller.add_takeoff_task(meta["altitude"])
    elif command == "move":
        controller.add_linear_movement_task(direction, meta["time"], priority)
    return True


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
            logging.error("Unexpected error, killing drone")
            debug_add_task(controller, "exit", {})
            return False
    elif args.routine:
        # If in production mode, starting or stopping drone is only option
        # get push data and check if start or kill
        command = data["command"].lower()
        if command == "start":
            # start routine
            start_ai(args.routine)
        elif command == "kill":
            # force into land
            kill_ai(controller)

        return "routine " + args.routine + " in progress"


def tcp_thread(args, controller):
    try:
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5005
        BUFFER_SIZE = 1024

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        set_keepalive_osx(s)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)

        conn, addr = s.accept()
        print('Connection address:', addr)
        while True:
            data = conn.recv(BUFFER_SIZE)
            print("received data:", data)
            if data:
                succ = add_task(args, controller, json.loads(data))
                if succ:
                    conn.send("success")
                else:
                    logging.info("Ending session")
                    conn.close()
    except socket.error:
        # kill DroneController
        print("Killing drone because of connection loss")


def main():
    # Get Command Line Arguments
    args = parse_args()

    # Establish controller
    # controller = DroneController(c.Drones.LEONARDO_SIM)
    # Run Flask server on seperate thread
    # server_thread = threading.Thread(
    #     target=tcp_thread, args=(args, controller))
    # server_thread.daemon = True

    # server_thread.start()
    # controller.run()
    tcp_thread(args, None)

    # After controller has stopped, exit Flask server.
    sys.exit(0)


if __name__ == "__main__":
    main()
