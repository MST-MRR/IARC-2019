"""Provides a continuous command line prompt for testing drone capabilities."""
import argparse
import sys
import threading
import traceback

from flight.drone.drone_controller import DroneController
from flight import constants
import flightconfig as config

PROMPT_FOR_COMMAND = '> '

# These values subject to change if encoding changes
INT_MAX = 255   # Maximum encodable int value ("FF")
INT_MIN = 0     # Minimum encodable int value ("00")

def main():
    # Make the controller object
    controller = DroneController(constants.Drones.LEONARDO)

    # Make a thread whose target is a command line interface
    input_thread = threading.Thread(
        target=input_loop, args=(controller,))

    # Don't prevent program termination if main thread ends
    input_thread.daemon = True

    input_thread.start()

    controller.run()


class ExitRequested(Exception):
    """Raised when the input loop should stop."""
    pass


def create_command_parser():
    """Returns an object which can parse commands given in english."""
    descr = "Parse english commands into executable tasks."
    parser = argparse.ArgumentParser(description=descr)

    # Outer argument: priority
    parser.add_argument('--priority',
        dest='priority',
        action=store_priority(),
        default=constants.Priorities.MEDIUM,
        help='the priority of the task')

    # Enable sub-parsing capabilities
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    # Exit sub-parser (has no arguments)
    parser_exit = subparsers.add_parser('exit', help='exit help')

    # Land sub-parser (has no arguments)
    parser_land = subparsers.add_parser('land', help='land help')

    # Takeoff sub-parser
    parser_takeoff = subparsers.add_parser('takeoff', help='takeoff help')
    parser_takeoff.add_argument('--altitude',
        dest='altitude',
        action=store_int(),
        default=config.DEFAULT_ALTITUDE,
        help='altitude to take off to')

    # Linear movement sub-parser
    parser_linear_move = subparsers.add_parser('move', help='move help')
    parser_linear_move.add_argument('-d', '--duration',
        dest='duration',
        action=store_int(),
        required=True,
        help='altitude to maintain during move')
    parser_linear_move.add_argument('--direction',
        dest='direction',
        action=store_direction(),
        required=True,
        help='direction to move in')
    parser_linear_move.add_argument('--altitude',
        dest='altitude',
        default=config.DEFAULT_ALTITUDE,
        action=store_int(),
        help='altitude to maintain during move')

    # Hover sub-parser
    parser_hover = subparsers.add_parser('hover', help='hover help')
    parser_hover.add_argument('--duration',
        dest='duration',
        action=store_int(),
        required=True,
        help='altitude to maintain during hover')
    parser_hover.add_argument('--altitude',
        dest='altitude',
        action=store_int(),
        default=config.DEFAULT_ALTITUDE,
        help='altitude to maintain during hover')

    return parser


# Custom arg parser "actions" are below
# See https://stackoverflow.com/questions/8632354/python-argparse-custom-actions-with-additional-arguments-passed
# for information on custom actions
def store_direction():
    """Converts english direction to Direction enum attribute."""
    class customAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            try:
                setattr(args, self.dest, get_direction(values))
            except:
                msg = 'Invalid direction - must be "forward", "back", "left" \
                    or "right"'
                raise argparse.ArgumentTypeError(msg)
    return customAction


def store_priority():
    """Converts english priority to Priority enum attribute."""
    class customAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            try:
                setattr(args, self.dest, get_priority(values))
            except:
                msg = 'Invalid priority - must be "low", "medium", or "high"'
                raise argparse.ArgumentTypeError(msg)
    return customAction


def store_int():
    """Converts english integer to an int object."""
    class customAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            try:
                converted_int = int(values)
                # Check that int is within acceptable range
                if converted_int < INT_MIN or converted_int > INT_MAX:
                    raise Exception
            except:
                msg = 'Value must be an integer between 0 and 255'
                raise argparse.ArgumentTypeError(msg)
            setattr(args, self.dest, converted_int)
    return customAction


def store_float():
    """Converts english floating point number to an float object.

    Notes
    -----
    Currently unused because encoding space too small
    """
    class customAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            try:
                converted_float = float(values)
                # TODO: Check value range
            except:
                raise argparse.ArgumentTypeError('Value must be a floating point number')
            setattr(args, self.dest, converted_float)
    return customAction


def input_loop(controller):
    """Simple command line interface to drone controller.

    """
    parser = create_command_parser()
    while True:
        try:
            raw_args = raw_input(PROMPT_FOR_COMMAND).lower().split()
            parsed_args = parser.parse_args(args=raw_args)
            function = COMMAND_TO_FUNCTION[parsed_args.command]
            function(controller, parsed_args)
        except SystemExit:
            # Incorrect arguments - help displayed
            continue
        except argparse.ArgumentTypeError as e:
            print e
        except ExitRequested as e:
            print('Ending input loop.')
            return
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                        limit=2, file=sys.stdout)
            continue


def get_priority(priority):
    """Gets priority level from a string.

    Parameters
    ----------
    priority : one of {'high', 'medium', 'low'}
        The priority to be tranlated into enum value.
    """
    key = priority.upper()
    if hasattr(constants.Priorities, key):
        converted_form = getattr(constants.Priorities, key)
    else:
        raise TypeError(
            'Expected value for type {}, got {}.'.format(
                type(constants.Priorities).__name__, priority))

    return converted_form


def get_direction(direction):
    """Gets direction from a string.

    Parameters
    ----------
    direction : one of {'forward', 'backward', 'left', 'right}
        The direction to be tranlated into enum value.
    """
    key = direction.upper()
    if hasattr(constants.Directions, key):
        converted_form = getattr(constants.Directions, key)
    else:
        raise TypeError(
            'Expected value for type {}, got {}.'.format(
                type(constants.Directions).__name__, direction))

    return converted_form


# NOTE: the following add_xyz functions encode and decode the message since
# this implementation is not using networked flight. This CLI is meant to be
# migrated to the server code, where each command will be encoded, sent to a
# drone, and then decoded on the drone.

def add_exit_task(controller, namespace):
    """Adds an exit task to the drone controller.

    Parameters
    ----------
    controller : flight.drone.DroneController
        The drone controller.
    namespace : argparse.Namespace
        Contains parameter names mapped to values.
    """
    msg_enc = controller.task_factory.exit_task_encode(priority=namespace.priority)
    print msg_enc
    msg_dec = controller.task_factory.decode(msg_enc)
    print msg_dec
    controller.add_task(msg_dec)
    raise ExitRequested # Tell input loop to stop

def add_land_task(controller, namespace):
    """Adds a land task to the drone controller.

    Parameters
    ----------
    controller : flight.drone.DroneController
        The drone controller.
    namespace : argparse.Namespace
        Contains parameter names mapped to values.
    """
    msg_enc = controller.task_factory.land_task_encode(priority=namespace.priority)
    print msg_enc
    msg_dec = controller.task_factory.decode(msg_enc)
    print msg_dec

    controller.add_task(msg_dec)


def add_takeoff_task(controller, namespace):
    """Adds a takeoff task to the drone controller.

    Parameters
    ----------
    controller : flight.drone.DroneController
        The drone controller.
    namespace : argparse.Namespace
        Contains parameter names mapped to values.
    """
    msg_enc = controller.task_factory.takeoff_task_encode(priority=namespace.priority,
            altitude=namespace.altitude)
    print msg_enc
    msg_dec = controller.task_factory.decode(msg_enc)
    print msg_dec
    controller.add_task(msg_dec)


def add_linear_move_task(controller, namespace):
    """Adds a linear movement task to the drone controller.

    Parameters
    ----------
    controller : flight.drone.DroneController
        The drone controller.
    namespace : argparse.Namespace
        Contains parameter names mapped to values.
    """
    msg_enc = controller.task_factory.linear_movement_task_encode(priority=namespace.priority,
            duration=namespace.duration,
            direction=namespace.direction,
            altitude=namespace.altitude)
    print msg_enc
    msg_dec = controller.task_factory.decode(msg_enc)
    print msg_dec
    controller.add_task(msg_dec)


def add_hover_task(controller, namespace):
    """Adds a hover task to the drone controller.

    Parameters
    ----------
    controller : flight.drone.DroneController
        The drone controller.
    namespace : argparse.Namespace
        Contains parameter names mapped to values.
    """
    msg_enc = controller.task_factory.hover_task_encode(priority=namespace.priority,
            duration=namespace.duration,
            altitude=namespace.altitude)
    print msg_enc
    msg_dec = controller.task_factory.decode(msg_enc)
    print msg_dec
    controller.add_task(msg_dec)

# Maps command name (set in argparser) to function for adding task
COMMAND_TO_FUNCTION = {
    'exit': add_exit_task,
    'land': add_land_task,
    'takeoff': add_takeoff_task,
    'move': add_linear_move_task,
    'hover': add_hover_task
}

if __name__ == '__main__':
    main()
