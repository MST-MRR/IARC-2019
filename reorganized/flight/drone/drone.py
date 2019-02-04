import dronekit
import logging
import time
import threading
from math import radians, sin, cos
from pymavlink import mavutil

from ..Utilities import constants as c
from ..Utilities import dronekit_wrappers
from ..Utilities.helper import current_thread_name
from ..Utilities.timer import Timer

class Drone(dronekit.Vehicle):
    """Interface to drone and to sensors.

    Attributes
    ----------
    _logger
        Write messages to command line.
    """

    def __init__(self):
        self._connected = False
        self._logger = logging.getLogger(__name__)e

    @property
    def id(self):
        """Get the drone's id"""
        return self._id

    @id.setter
    def id(self, identifier):
        """Set the drone's id."""
        self._id = identifier

    def set_attitude(self, roll, pitch, yaw, thrust):
        msg = _make_attitude_message(roll, pitch, yaw, thrust)
        self.send_mavlink(msg)

    def send_velocity(self, north, east, down):
        msg = _make_velocity_message(north, east, down)
        self.send_mavlink(msg)

    def _make_velocity_message(self, north, east, down):
        """Construct a mavlink message for sending velocity.

        Parameters
        ----------

        Returns
        -------
        MAVLink_message (a DroneKit object)
            Message which moves the drone at a certain velocity.

        see http://python.dronekit.io/examples/guided-set-speed-yaw-demo.html#send-global-velocity
        """
        return self.message_factory.set_position_target_global_int_encode(
            0,       # time_boot_ms (not used)
            0, 0,    # target system, target component
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
            0b0000111111000111, # type_mask (only speeds enabled)
            0, # lat_int - X Position in WGS84 frame in 1e7 * meters
            0, # lon_int - Y Position in WGS84 frame in 1e7 * meters
            0, # alt - Altitude in meters in AMSL altitude(not WGS84 if absolute or relative)
            # altitude above terrain if GLOBAL_TERRAIN_ALT_INT
            velocity_x, # X velocity in NED frame in m/s
            velocity_y, # Y velocity in NED frame in m/s
            velocity_z, # Z velocity in NED frame in m/s
            0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
            0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    def _make_attitude_message(self, roll, pitch, yaw, thrust):
        """Set the attitude of the drone."""
        # Thrust >  0.5: Ascend
        # Thrust == 0.5: Hold the altitude
        # Thrust <  0.5: Descend
        return self.message_factory.set_attitude_target_encode(
            0, # time_boot_ms
            1, # Target system
            1, # Target component
            0b00000000, # Type mask: bit 1 is LSB
            _to_quaternion(roll_angle, pitch_angle), # Quaternion
            0, # Body roll rate in radian
            0, # Body pitch rate in radian
            radians(yaw_rate), # Body yaw rate in radian
            thrust  # Thrust
        )

    def _to_quaternion(roll = 0.0, pitch = 0.0, yaw = 0.0):
        """Convert degrees to quaternions.

        See https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles#Source_Code
        """
        t0 = cos(radians(yaw * 0.5))
        t1 = sin(radians(yaw * 0.5))
        t2 = cos(radians(roll * 0.5))
        t3 = sin(radians(roll * 0.5))
        t4 = cos(radians(pitch * 0.5))
        t5 = sin(radians(pitch * 0.5))

        w = t0 * t2 * t4 + t1 * t3 * t5
        x = t0 * t3 * t4 - t1 * t2 * t5
        y = t0 * t2 * t5 + t1 * t3 * t4
        z = t1 * t2 * t4 - t0 * t3 * t5

        return [w, x, y, z]
