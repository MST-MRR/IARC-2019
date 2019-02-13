from flight.drone.drone_controller import DroneController
from flight import constants as c
from flight import flightconfig as f

HOVERTASK_DURATION = 10

controller = DroneController(c.Drones.LEONARDO_SIM)

controller.add_takeoff_task(f.DEFAULT_ALTITUDE)
controller.add_hover_task(
    f.DEFAULT_ALTITUDE, HOVERTASK_DURATION, c.Priorities.MEDIUM)
controller.add_land_task(c.Priorities.MEDIUM)

controller.run()
