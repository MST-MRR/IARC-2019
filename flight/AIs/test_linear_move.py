from flight.drone.drone_controller import DroneController
from flight import constants as c
from flight import flightconfig as f

HOVER_DURATION = 5
MOVE_DURATION = 5

controller = DroneController(c.Drones.LEONARDO_SIM)

controller.add_takeoff_task(f.DEFAULT_ALTITUDE)
controller.add_hover_task(
    f.DEFAULT_ALTITUDE, HOVER_DURATION, c.Priorities.MEDIUM)
controller.add_linear_movement_task(c.Directions.FORWARD, MOVE_DURATION)
controller.add_hover_task(
    f.DEFAULT_ALTITUDE, HOVER_DURATION, c.Priorities.MEDIUM)
controller.add_land_task()
controller.add_exit_task()

controller.run()