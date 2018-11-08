import abc
import dronekit
from dronekit import VehicleMode
import time
import math
from pymavlink import mavutil

# Description:
#    Wraps DroneKit vehicle and sensors.
# Attributes:
#    int id
#    dronekit.Vehicle drone
#    list<Device> devices
class Drone(object):
    __metaclass__ = abc.ABCMeta
    
    # Static variables
    DEFAULT_VELOCITY = 1
    VELOCITY_THRESHOLD = 5 # never let the drone go faster than 5 m/s for safety (is this a good number?)

    def __init__(self):
        self.devices = []

    def connect(self):
        # Connect to the drone
        self.vehicle = dronekit.connect("tcp:127.0.0.1:5762", wait_ready=True)

    def arm(self):
        while not self.vehicle.is_armable:
            print("Waiting...\n")
            time.sleep(1.0)
        self.vehicle.mode = VehicleMode("GUIDED")

        while not self.vehicle.armed:
            self.vehicle.armed = True
            time.sleep(1)

    def takeoff(self, targetAltitude):
        DEFAULT_TAKEOFF_THRUST = 0.7
        SMOOTH_TAKEOFF_THRUST = 0.6

        thrust = DEFAULT_TAKEOFF_THRUST
        while True:
            current_altitude = self.vehicle.rangefinder.distance
            if current_altitude >= targetAltitude*0.95: # Trigger just below target alt.
                print("Reached target altitude")
                break
            elif current_altitude >= targetAltitude*0.6:
                thrust = SMOOTH_TAKEOFF_THRUST
            self.set_attitude(thrust = thrust)
            time.sleep(0.2)

    def land(self):
        while (not self.vehicle.mode == VehicleMode("LAND")):
            self.vehicle.mode = VehicleMode("LAND")

    # Should fill devices list with all of the devices a particular drone has
    @abc.abstractmethod
    def loadDevices(self):
        return

    # Movement methods (basic implementation provided):
    @abc.abstractmethod
    def forward(self, velocity = DEFAULT_VELOCITY, duration = 1, distance = None):
        if (velocity > self.VELOCITY_THRESHOLD):
            raise Exception('Velocity threshold exceeded')
        
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')

        # Other checks?

        # If distance is set, fly that distance
        if distance is not None:
            duration = distance / self.DEFAULT_VELOCITY
            self.send_global_velocity(-1 * self.DEFAULT_VELOCITY, 0, 0, duration)
        # Else, fly at given velocity for given seconds
        else:
            self.send_global_velocity(-1 * velocity, 0, 0, duration)

    @abc.abstractmethod
    def backward(self, velocity = DEFAULT_VELOCITY, duration = 1, distance = None):
        if (velocity > self.VELOCITY_THRESHOLD):
            raise Exception('Velocity threshold exceeded')
            
            
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')

        # Other checks?

        # If distance is set, fly that distance
        if distance is not None:
            duration = distance / self.DEFAULT_VELOCITY
            self.send_global_velocity(self.DEFAULT_VELOCITY, 0, 0, duration)
        # Else, fly at given velocity for given seconds
        else:
            self.send_global_velocity(velocity, 0, 0, duration)

    @abc.abstractmethod
    def left(self, velocity = DEFAULT_VELOCITY, duration = 1, distance = None):
        if (velocity > self.VELOCITY_THRESHOLD):
            raise Exception('Velocity threshold exceeded')
            
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')

        # Other checks?

        # If distance is set, fly that distance
        if distance is not None:
            duration = distance / self.DEFAULT_VELOCITY
            self.send_global_velocity(0, self.DEFAULT_VELOCITY, 0, duration)
        # Else, fly at given velocity for given seconds
        else:
            self.send_global_velocity(0, velocity, 0, duration)

    @abc.abstractmethod
    def right(self, velocity = DEFAULT_VELOCITY, duration = 1, distance = None):
        if (velocity > self.VELOCITY_THRESHOLD):
            raise Exception('Velocity threshold exceeded')
            
        # Other checks?

        # If distance is set, fly that distance
        if distance is not None:
            duration = distance / self.DEFAULT_VELOCITY
            self.send_global_velocity(0, -1 * self.DEFAULT_VELOCITY, 0, duration)
        # Else, fly at given velocity for given seconds
        else:
            self.send_global_velocity(0, -1 * velocity, 0, duration)


    @abc.abstractmethod
    def up(self, velocity = DEFAULT_VELOCITY, duration = 1, distance = None):
        if (velocity > self.VELOCITY_THRESHOLD):
            raise Exception('Velocity threshold exceeded')
            
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')

        # Other checks?

        # If distance is set, fly that distance
        if distance is not None:
            duration = distance / self.DEFAULT_VELOCITY
            self.send_global_velocity(0, 0, self.DEFAULT_VELOCITY, duration)
        # Else, fly at given velocity for given seconds
        else:
            self.send_global_velocity(0, 0, velocity, duration)


    @abc.abstractmethod
    def down(self, velocity = DEFAULT_VELOCITY, duration = 1, distance = None):
        if (velocity > self.VELOCITY_THRESHOLD):
            raise Exception('Velocity threshold exceeded')
            
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')

        # Other checks?

        # If distance is set, fly that distance
        if distance is not None:
            duration = distance / self.DEFAULT_VELOCITY
            self.send_global_velocity(0, 0, -1  * self.DEFAULT_VELOCITY, duration)
        # Else, fly at given velocity for given seconds
        else:
            self.send_global_velocity(0, 0, -1 * velocity, duration)


    # Tells the drone to move with the given velocities in the x, y, and z direction
    # for a specifies number of seconds.
    def send_global_velocity(self, velocity_x, velocity_y, velocity_z, duration):
        """
        Move vehicle in direction based on specified velocity vectors.
        """
        msg = self.vehicle.message_factory.set_position_target_global_int_encode(
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

        # send command to vehicle on 1 Hz cycle
        for x in range(0,duration):
            self.vehicle.send_mavlink(msg)
            time.sleep(1)

    def set_attitude(self, roll_angle = 0.0, pitch_angle = 0.0, yaw_rate = 0.0, thrust = 0.5, duration = 0):
        """
        Note that from AC3.3 the message should be re-sent every second (after about 3 seconds
        with no message the velocity will drop back to zero). In AC3.2.1 and earlier the specified
        velocity persists until it is canceled. The code below should work on either version
        (sending the message multiple times does not cause problems).
        """

        """
        The roll and pitch rate cannot be controllbed with rate in radian in AC3.4.4 or earlier,
        so you must use quaternion to control the pitch and roll for those vehicles.
        """

        # Thrust >  0.5: Ascend
        # Thrust == 0.5: Hold the altitude
        # Thrust <  0.5: Descend
        msg = self.vehicle.message_factory.set_attitude_target_encode(
            0, # time_boot_ms
            1, # Target system
            1, # Target component
            0b00000000, # Type mask: bit 1 is LSB
            self.to_quaternion(roll_angle, pitch_angle), # Quaternion
            0, # Body roll rate in radian
            0, # Body pitch rate in radian
            math.radians(yaw_rate), # Body yaw rate in radian
            thrust  # Thrust
        )
        self.vehicle.send_mavlink(msg)

        start = time.time()
        while time.time() - start < duration:
            self.vehicle.send_mavlink(msg)
            time.sleep(0.1)

    def to_quaternion(self, roll = 0.0, pitch = 0.0, yaw = 0.0):
        """
        Convert degrees to quaternions
        """
        t0 = math.cos(math.radians(yaw * 0.5))
        t1 = math.sin(math.radians(yaw * 0.5))
        t2 = math.cos(math.radians(roll * 0.5))
        t3 = math.sin(math.radians(roll * 0.5))
        t4 = math.cos(math.radians(pitch * 0.5))
        t5 = math.sin(math.radians(pitch * 0.5))

        w = t0 * t2 * t4 + t1 * t3 * t5
        x = t0 * t3 * t4 - t1 * t2 * t5
        y = t0 * t2 * t5 + t1 * t3 * t4
        z = t1 * t2 * t4 - t0 * t3 * t5

        return [w, x, y, z]

