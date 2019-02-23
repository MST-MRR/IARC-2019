from .. import constants as c
import config

HOVER_DURATION = 10


def test_hover(controller):
    """

        Tests the Hover Task

        Parameters
        ----------
        controller : flight.drone.drone_controller.DroneController
            Drone controller object used for handling tasks

    """
    controller.add_takeoff_task(config.DEFAULT_ALTITUDE)
    controller.add_hover_task(
        config.DEFAULT_ALTITUDE, HOVER_DURATION, c.Priorities.MEDIUM)
    controller.add_land_task(c.Priorities.MEDIUM)
