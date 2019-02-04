from dronekit import connect, VehicleMode
import logging
import coloredlogs
from time import sleep
import traceback
import sys

import exceptions
from drone import Drone
from ..tasks.task_base import TaskBase
from .. import constants as c
from ..tasks.hover_task import HoverTask
from ..tasks.takeoff_task import TakeoffTask
from ..tasks.linear_movement_task import LinearMovementTask
from ..utils.priority_queue import PriorityQueue
from ..utils.timer import Timer

class DroneController(object):
    """Base class for controlling the actions of a drone.

    Responsible for managing the execution of tasks, maintaining a queue of
    instructions, and responding gracefully to emergency landing events.

    Attributes
    ----------
    _id : int
        Identification number used by the swarm controller to distinguish
        between the drones.
    instruction_queue : list of InstructionBase subclass
        A priority queue holding instruction sent from the swarm controller or
        inter-drone communication.
    current_instruction : InstructionBase subclass
        The instruction currently being processed.
    task : TaskBase subclass
        The task the drone is currently working on.
    """

    def __init__(self, drone):
        """drone is a member of the Drone enum"""
        self._task_queue = PriorityQueue()
        self._current_task = None

        self._logger = logging.getLogger(__name__)
        coloredlogs.install(level=logging.INFO)

        self._logger.info('Connecting...')
        connection_string = c.CONNECTION_STR_DICT[drone]
        self._drone = connect(
            connection_string, wait_ready=True,
            heartbeat_timeout=c.HEARTBEAT_TIMEOUT, status_printer=None,
            vehicle_class=Drone)
        self._logger.info('Connected')

    def run(self):
        self._logger.info('Controller starting')

        try:
            # Arm the drone for flight
            self._arm()

            # NOTE: the only way to stop the loop is to raise an exceptions,
            # such as with a keyboard interrupt
            while True:
                self._do_safety_checks()
                self._update()
                sleep(c.DELAY_INTERVAL)

        except BaseException as e:
            self._logger.warning('Emergency landing initiated!')

            # Only print stack trace for completely unexpected things
            self._logger.critical(type(e).__name__)
            if c.DEBUG is True:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)

            # Land the drone
            self._land()
            self._logger.info('Controller exiting')

    def add_hover_task(self, altitude, duration, priority=c.Priorities.LOW):
        new_task = HoverTask(self._drone, altitude, duration)
        self._task_queue.push(priority, new_task)

    def add_takeoff_task(self, altitude):
        new_task = TakeoffTask(self._drone, altitude)
        self._task_queue.push(c.Priorities.HIGH, new_task)

    def add_linear_movement_task(
            self, direction, duration, priority=c.Priorities.MEDIUM):
        new_task = LinearMovementTask(self._drone, direction, duration)
        self._task_queue.push(c.Priorities.HIGH, new_task)

    def _update(self):
        """Execute one iteration of control logic.

        Checks that a land event has not been set and executes the
        next iteration of the current task, if one exists.

        Returns
        -------
        bool
            False if the update should continue to be called and false
            otherwise
        """
        if self._current_task is not None:
            # Do one iteration of whichever task we are in
            result = self._current_task.perform()

            # If we are done, set the task to None so that
            # we can move on to the next instruction
            if result:
                # We are done with the task
                self._logger.info('Finished {}...'.format(self._current_task))
                self._task_queue.pop()

        prev_task = self._current_task

        self._current_task = self._task_queue.top()

        if prev_task is not self._current_task:
            self._logger.info('Starting {}...'.format(self._current_task))

        # If there are no more tasks, begin to hover.
        if self._current_task is None:
            self.add_hover_task(c.DEFAULT_ALTITUDE, 480)

    def _do_safety_checks(self):
        """Check for exceptional conditions."""
        if self._drone.airspeed > c.SPEED_THRESHOLD:
            raise exceptions.VelocityExceededThreshold()

        if (self._drone.rangefinder.distance > c.MAXIMUM_ALLOWED_ALTITUDE):
            raise exceptions.AltitudeExceededThreshold()

        if (self._drone.rangefinder.distance
                < c.RANGEFINDER_MIN - c.RANGEFINDER_EPSILON -.5):
            raise exceptions.RangefinderMalfunction()

        # TODO: Add more safety checks here

    def _arm(self, timeout=c.DEFAULT_ARM_TIMEOUT, mode=c.Modes.GUIDED.value):
        """Arm the drone for flight.

        Upon successfully arming, the drone is now suitable to take off. The
        drone should be connected before calling this function.

        Parameters
        ----------
        timeout : int, optional
            The duration in seconds that arming should be attempted before
            timing out
        mode : {GUIDED}, optional

        Returns
        -------
        bool
            True if successfully armed and false otherwise.

        Notes
        -----
        Only guided mode is currently supported.
        """
        self._drone.mode = VehicleMode(mode)

        self._logger.info('Arming...')
        timer = Timer()
        while (not self._drone.armed) and (timer.elapsed < timeout):
            self._drone.armed = True
            sleep(c.ARM_RETRY_DELAY)

        status_msg = 'Failed to arm' if not self._drone.armed else 'Armed'
        logging_function = (self._logger.info if self._drone.armed
            else self._logger.error)
        logging_function('{}'.format(status_msg))

    def _land(self):
        """Land the drone.

        The flight mode is set to land.

        Returns
        -------
        finished : threading.Event
            The finished event is set upon successful landing
        """

        land_mode = VehicleMode(c.Modes.LAND.value)

        self._logger.info('Starting land...')
        while not self._drone.mode == land_mode:
            self._drone.mode = land_mode
        self._logger.info('Finished land')

        self._logger.info('Waiting for disarm...')
        while self._drone.armed:
            sleep(c.DELAY_INTERVAL)
        self._logger.info('Disarm complete')
