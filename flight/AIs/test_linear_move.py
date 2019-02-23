from .. import constants as c
import config

HOVER_DURATION = 5
MOVE_DURATION = 5


def test_linear_move(controller):
    """

        Tests the LinearMovement Task

        Parameters
        ----------
        controller : flight.drone.drone_controller.DroneController
            Drone controller object used for handling tasks

    """
    controller.add_takeoff_task(config.DEFAULT_ALTITUDE)
    controller.add_hover_task(
        config.DEFAULT_ALTITUDE, HOVER_DURATION, c.Priorities.MEDIUM)
    controller.add_linear_movement_task(c.Directions.FORWARD, MOVE_DURATION)
    controller.add_hover_task(
        config.DEFAULT_ALTITUDE, HOVER_DURATION, c.Priorities.MEDIUM)
    controller.add_land_task()
    controller.add_exit_task()
