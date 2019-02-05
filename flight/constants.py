"""
All of the constant values used across all of the scripts are located here.
"""

from enum import Enum

class Drones(Enum):
    LEONARDO_SIM = "Leonardo_Sim"
    LEONARDO = "Leonardo"

CONNECTION_STR_DICT = {
        Drones.LEONARDO_SIM : 'tcp:127.0.0.1:5762',
        Drones.LEONARDO: '/dev/serial/by-id/usb-3D_Robotics_PX4_FMU_v2.x_0-if00'
        }
"""Drone connection strings.

Notes
-----
See http://python.dronekit.io/guide/connecting_vehicle.html
and http://ardupilot.org/dev/docs/learning-ardupilot-the-example-sketches.html.
"""

# Set to true for more detailed error messages and backtraces
DEBUG = True

# How high in meters the drone will default flight
DEFAULT_ALTITUDE = 1
# How fast (in meters/s) to move by default
DEFAULT_SPEED = 0.50
# Maximum speed (in meters/s) before being considered unsafe
SPEED_THRESHOLD = 1
# Maximum altitude (in meters) before being considered unsafe
MAXIMUM_ALLOWED_ALTITUDE = 1.5
# How often to run safety checks
SAFETY_CHECKS_DELAY = 0.5


class Priorities(Enum):
    """Constants for differentiating the priority of items.

    Notes
    -----
    Values are based on heapq, with is a min-heap.
    """
    LOW = 3
    MEDIUM = 2
    HIGH = 1


# DroneKit Vehicle Modes
class Modes(Enum)  :
    """The various modes of flight."""
    GUIDED = "GUIDED"
    LAND = "LAND"
    FLOW_HOLD = "FLOW_HOLD"
    FOLLOW = "FOLLOW"

class Directions(Enum):
    """Directions along each axis.

    Notes
    -----
    RIGHT => positive x
    LEFT => negative x
    FORWARD => positive y
    BACKWARD => negative y
    """
    UP = (0, 0, 1)
    DOWN = (0, 0, -1)
    LEFT = (0, 1, 0)
    RIGHT = (0, -1, 0)
    FORWARD = (1, 0, 0)
    BACKWARD = (-1, 0, 0)

# Thrust level during takeoff
DEFAULT_TAKEOFF_THRUST = 0.7
# Consider takeoff complete after reaching this percent of target takeoff
# altitude
PERCENT_TARGET_ALTITUDE = 0.3
# Expands or contracts time calculations (divide 1 by your average real-time
# factor in Gazebo simulator)
SIMULATION_MULTIPLIER = 1

# How often to run main control loop
DELAY_INTERVAL = 0.1
# How often to retry arming during arm function
ARM_RETRY_DELAY = 1
# How long to wait before timing out a connection attempt
CONNECT_TIMEOUT = 60

DEFAULT_HOVER_DURATION = 480
