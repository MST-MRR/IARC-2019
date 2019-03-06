"""Provides a continuous command line prompt for testing drone capabilities."""
import argparse
import sys
import threading
import traceback


from flight.tasks.encoder import Encoder
from flight.tasks.decoder import Decoder


import config
from flight.drone.drone_controller import DroneController
from flight import constants
import flight.tasks

PROMPT_FOR_COMMAND = '> '

def main():

    parser = create_program_input_parser()

    args = parser.parse_args()

    if args.sim:
        config.IS_SIMULATION = True
        config.CONNECTION_STRING = constants.CONNECTION_STR_DICT[constants.Drones.LEONARDO_SIM]

    msg = Encoder.encode(flight.tasks.LinearMovement, constants.Priorities.HIGH,
        duration=5.5, direction=constants.Directions.BACKWARD, altitude=3.14)

    task = Decoder.decode(msg)

    print task

    """
    # Make the controller object
    controller = DroneController()

    input_thread = threading.Thread(
        target=input_loop, args=(controller,))

    # Don't prevent program termination if main thread ends
    input_thread.daemon = True

    input_thread.start()

    controller.run()
    """


class ExitRequested(Exception):
    """Raised when the input loop should stop."""
    pass


def create_program_input_parser():
    """Creates a parser for argument given to this program, testing_cli.py."""
    descr = "Configure the testing command line interface."
    parser = argparse.ArgumentParser(description=descr)

    parser.add_argument('--sim',
        dest='sim',
        action='store_true',
        default=False,
        help='whether or not the drone is simulated')

    return parser


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
        action=store_float(),
        default=config.DEFAULT_ALTITUDE,
        help='altitude to take off to')

    # Linear movement sub-parser
    parser_linear_move = subparsers.add_parser('move', help='move help')
    parser_linear_move.add_argument('--duration',
        dest='duration',
        action=store_float(),
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
        action=store_float(),
        help='altitude to maintain during move')

    # Hover sub-parser
    parser_hover = subparsers.add_parser('hover', help='hover help')
    parser_hover.add_argument('--duration',
        dest='duration',
        action=store_float(),
        required=True,
        help='altitude to maintain during hover')
    parser_hover.add_argument('--altitude',
        dest='altitude',
        action=store_float(),
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


def store_float():
    """Converts english floating point number to an float object."""
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

    Parameters
    ----------
    Controller : flight.drone.DroneController
        The drone controller that tasks should be given to.
    """
    parser = create_command_parser()
    while True:
        try:
            raw_args = raw_input(PROMPT_FOR_COMMAND).lower().split()
            parsed_args = parser.parse_args(args=raw_args)
            function = COMMAND_TO_FUNCTION[parsed_args.command]
            function(controller, parsed_args)
        except SystemExit: # argparse throws this when given invalid input
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


def add_exit_task(controller, namespace):
    """Adds an exit task to the drone controller.

    Parameters
    ----------
    controller : flight.drone.DroneController
        The drone controller.
    namespace : argparse.Namespace
        Contains parameter names mapped to values.
    """
    task = (namespace.priority, flight.tasks.Exit())
    controller.add_task(task)
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
    task = (namespace.priority, flight.tasks.Land())
    controller.add_task(task)


def add_takeoff_task(controller, namespace):
    """Adds a takeoff task to the drone controller.

    Parameters
    ----------
    controller : flight.drone.DroneController
        The drone controller.
    namespace : argparse.Namespace
        Contains parameter names mapped to values.
    """
    if config.IS_SIMULATION:
        task = (namespace.priority, flight.tasks.TakeoffSim(altitude=namespace.altitude))
    else:
        task = (namespace.priority, flight.tasks.Takeoff(altitude=namespace.altitude))
    controller.add_task(task)


def add_linear_move_task(controller, namespace):
    """Adds a linear movement task to the drone controller.

    Parameters
    ----------
    controller : flight.drone.DroneController
        The drone controller.
    namespace : argparse.Namespace
        Contains parameter names mapped to values.
    """
    task = (namespace.priority, flight.tasks.LinearMovement(
            duration=namespace.duration,
            direction=namespace.direction,
            altitude=namespace.altitude
            ))
    controller.add_task(task)


def add_hover_task(controller, namespace):
    """Adds a hover task to the drone controller.

    Parameters
    ----------
    controller : flight.drone.DroneController
        The drone controller.
    namespace : argparse.Namespace
        Contains parameter names mapped to values.
    """
    task = (namespace.priority, flight.tasks.Hover(
            duration=namespace.duration,
            altitude=namespace.altitude
            ))
    controller.add_task(task)


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
