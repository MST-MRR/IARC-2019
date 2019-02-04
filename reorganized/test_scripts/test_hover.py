from ..flight.drone.drone_controller import DroneController
from ..flight import constants as c

controller = DroneController(c.Drones.LEONARDO_SIM)

controller.add_takeoff_task(c.DEFAULT_ALTITUDE)
controller.add_hover_task(c.DEFAULT_ALTITUDE, c.DEFAULT_ALTITUDE)

controller.run()
