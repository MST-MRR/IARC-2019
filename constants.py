# Safety
DEFAULT_VELOCITY = 0.25
VELOCITY_THRESHOLD = 2  # never let the drone go faster than 1 m/s for safety (is this a good number?)
MINIMUM_ALLOWED_ALTITUDE = 0.5

# Connection-oriented
CONNECTION_STRING_SIMULATOR = "tcp:127.0.0.1:5762"
CONNECTION_STRING_REAL = "/dev/serial/by-id/usb-3D_Robotics_PX4_FMU_v2.x_0-if00"

# DroneKit Vehicle Modes
GUIDED = "GUIDED"
LAND = "LAND"

# Directions
UP = (0, 0, 1)
DOWN = (0, 0, -1)
LEFT = (0, 1, 0)
RIGHT = (0, -1, 0)
FORWARD = (-1, 0, 0)
BACKWARD = (1, 0, 0)

# Movement
DEFAULT_TAKEOFF_THRUST = 0.7
SMOOTH_TAKEOFF_THRUST = 0.6

# Sleep Times
TEN_MILI = 0.01
HUNDRED_MILI = 0.1
HALF_SEC = 0.5
SECOND = 1.0