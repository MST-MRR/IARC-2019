from dronekit import Vehicle
import logging
import time
import threading
from math import radians, sin, cos
from pymavlink import mavutil

from optical_flow_attribute import OpticalFlow
from .. import constants as c
from ..utils.timer import Timer

class Drone(Vehicle):
    """Interface to drone and its sensors.

    Attributes
    ----------
    _id : int
        A unique identifier for this drone.
    """

    def __init__(self, *args):
        super(Drone, self).__init__(*args)
        self._id = None
        self._logger = logging.getLogger(__name__)

        self._optical_flow = OpticalFlow()

        # Allow us to listen for optical flow dat
        @self.on_message('OPTICAL_FLOW')
        def listener(self, name, message):
            """
            The listener is called for messages that contain the string specified
            in the decorator,passing the vehicle, message name, and the message.
            """
            self._optical_flow.time_usec = message.time_usec
            self._optical_flow.sensor_id = message.sensor_id
            self._optical_flow.flow_x = message.flow_x
            self._optical_flow.flow_y = message.flow_y
            self._optical_flow.flow_comp_m_x = message.quality
            self._optical_flow.flow_comp_m_y = message.flow_comp_m_y
            self._optical_flow.quality = message.quality
            self._optical_flow.ground_distance = message.ground_distance

            # Notify all observers of new message (with new value)
            #   Note that argument `cache=False` by default so listeners
            #   are updaed with every new message
            self.notify_attribute_listeners('optical_flow', self._optical_flow)

    @property
    def optical_flow(self):
        """Get data from the optical flow sensor.

        Notes
        -----
        See optical_flow_attribute.py for what kind of data you can get.
        """
        return self._optical_flow

    @property
    def id(self):
        """Get the drone's id"""
        return self._id

    @id.setter
    def id(self, identifier):
        """Set the drone's id."""
        self._id = identifier

    def set_attitude(self, roll, pitch, yaw, thrust):
        """Set the drones attitude.

        Parameters
        ----------
        roll : double
            The roll angle.
        pitch : double
            The pitch angle.
        yaw : double
            The yaw rate.
        thrust : double between 0 and 1
            The thrust value.

        Notes
        -----
        If thrust < 0.5, the drone will lose altitude
        If thrust == 0.5, the drone will retain its altitude
        If thrust > 0.5, the drone will gain altitude
        """
        msg = self._make_attitude_message(roll, pitch, yaw, thrust)
        self.send_mavlink(msg)

    def send_velocity(self, north, east, down):
        """Send velocity to the drone.

        Parameters
        ----------
        north : double
        east : double
        down : double

        Notes
        -----
        This method used the NED coordinate system. Of note is that sending a
        positive value for down will make the drone lose altitude.
        """
        msg = self._make_velocity_message(north, east, down)
        self.send_mavlink(msg)

    def _make_velocity_message(self, north, east, down):
        """Construct a mavlink message for sending velocity.

        Parameters
        ----------
        north : double
        east : double
        down : double

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
            north, # X velocity in NED frame in m/s
            east, # Y velocity in NED frame in m/s
            down, # Z velocity in NED frame in m/s
            0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
            0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    def _make_attitude_message(self, roll, pitch, yaw, thrust):
        """Set the attitude of the drone.

        Parameters
        ----------
        roll : double
            The roll angle.
        pitch : double
            The pitch angle.
        yaw : double
            The yaw rate.
        thrust : double between 0 and 1
            The thrust value.
        """
        # Thrust >  0.5: Ascend
        # Thrust == 0.5: Hold the altitude
        # Thrust <  0.5: Descend
        return self.message_factory.set_attitude_target_encode(
            0, # time_boot_ms
            1, # Target system
            1, # Target component
            0b00000000, # Type mask: bit 1 is LSB
            self._to_quaternion(roll, pitch), # Quaternion
            0, # Body roll rate in radian
            0, # Body pitch rate in radian
            radians(yaw), # Body yaw rate in radian
            thrust  # Thrust
        )

    def _to_quaternion(self, roll=0.0, pitch=0.0, yaw=0.0):
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
