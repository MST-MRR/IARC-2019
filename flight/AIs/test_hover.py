from .. import constants as c
from ..drone.drone_controller import DroneController
from ... import config

HOVER_DURATION = 10

controller = DroneController(c.Drones.LEONARDO_SIM)

controller.add_takeoff_task(config.DEFAULT_ALTITUDE)
controller.add_hover_task(
    config.DEFAULT_ALTITUDE, HOVER_DURATION, c.Priorities.MEDIUM)
controller.add_land_task(c.Priorities.MEDIUM)

controller.run()
