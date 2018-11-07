import abc
import dronekit

# Description:
#    Wraps DroneKit vehicle and sensors.
# Attributes:
#    int id
#    dronekit.Vehicle drone
#    list<Device> devices
class Drone(object):
    __metaclass__ = abc.ABCMeta
    
    # Static variables
    MOVEMENT_COMPLETE = 0
    MOVEMENT_FAILED = 1
    DEFAULT_VELOCITY = 1
    VELOCITY_THRESHOLD = 5 # never let the drone go faster than 5 m/s for safety (is this a good number?)

    def __init__(self):
        self.id = 1 # should the drone set its own id or should the swarm controller give an id?
        self.devices = []

    def getId(self):
        return self.id

    def connect(self):
        # Connect to the drone
        self.vehicle = dronekit.connect("tcp:127.0.0.1:5762", wait_ready=True)
        print("\n Connected")

    def arm(self, vehicle):
        while not self.vehicle.is_armable:
            print("Waiting...\n")
            time.sleep(1.0)

        print("Arming motors\n")
        self.vehicle.mode = VehicleMode("GUIDED")

        while not vehicle.armed:
            self.vehicle.armed = True
            print("Waiting till armed")
            time.sleep(1)

    def takeoff(self):
        thrust = DEFAULT_TAKEOFF_THRUST
        while True:
            current_altitude = self.vehicle.rangefinder.distance
            if current_altitude >= aTargetAltitude*0.95: # Trigger just below target alt.
                print("Reached target altitude")
                break
            elif current_altitude >= aTargetAltitude*0.6:
                thrust = SMOOTH_TAKEOFF_THRUST
            set_attitude(self.vehicle, thrust = thrust)
            time.sleep(0.2)

    def land(self):
        print("Landing")
        while (not self.vehicle.mode == VehicleMode("LAND")):
            self.vehicle.mode = VehicleMode("LAND")

    # Should fill devices list with all of the devices a particular drone has
    @abc.abstractmethod
    def loadDevices(self):
        return

    # Movement methods (basic implementation provided):
    @abc.abstractmethod
    def forward(self, velocity, duration):
        if (velocity > self.VELOCITY_THRESHOLD):
            raise Exception('Velocity threshold exceeded')
        
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')
        # other checks?

        send_global_velocity(velocity, 0, 0, duration)
    @abc.abstractmethod
    def forward(self, distance):
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')
        # other checks?

        duration = distance / self.DEFAULT_VELOCITY
        send_global_velocity(DEFAULT_VELOCITY, 0, 0, duration)

    @abc.abstractmethod
    def backward(self, velocity, duration):
        if (velocity > self.VELOCITY_THRESHOLD):
            raise Exception('Velocity threshold exceeded')
            
            
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')

        send_global_velocity(-1 * velocity, 0, 0, duration)
    @abc.abstractmethod
    def backward(self, distance):
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')
        # other checks?

        duration = distance / self.DEFAULT_VELOCITY
        send_global_velocity(-1 * DEFAULT_VELOCITY, 0, 0, duration)

    @abc.abstractmethod
    def left(self, velocity, duration):
        if (velocity > self.VELOCITY_THRESHOLD):
            raise Exception('Velocity threshold exceeded')
            
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')

        send_global_velocity(0, velocity, 0, duration)
    @abc.abstractmethod
    def left(self, distance):
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')
        # other checks?

        duration = distance / self.DEFAULT_VELOCITY
        send_global_velocity(0, DEFAULT_VELOCITY, 0, duration)

    @abc.abstractmethod
    def right(self, velocity, duration):
        if (velocity > self.VELOCITY_THRESHOLD):
            raise Exception('Velocity threshold exceeded')
            
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')

        send_global_velocity(0, -1 * velocity, 0, duration)
    @abc.abstractmethod
    def right(self, distance):
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')
        # other checks?

        duration = distance / self.DEFAULT_VELOCITY
        send_global_velocity(0, -1 * DEFAULT_VELOCITY, 0, duration)

    @abc.abstractmethod
    def up(self, velocity, duration):
        if (velocity > self.VELOCITY_THRESHOLD):
            raise Exception('Velocity threshold exceeded')
            
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')

        send_global_velocity(0, 0, velocity, duration)
    @abc.abstractmethod
    def up(self, distance):
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')
        # other checks?

        duration = distance / self.DEFAULT_VELOCITY
        send_global_velocity(0, 0, DEFAULT_VELOCITY, duration)

    @abc.abstractmethod
    def down(self, velocity, duration):
        if (velocity > self.VELOCITY_THRESHOLD):
            raise Exception('Velocity threshold exceeded')
            
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')

        send_global_velocity(0, 0, -1 * velocity, duration)
    @abc.abstractmethod
    def down(self, distance):
        altitude = self.vehicle.rangefinder.distance
        if (altitude < 0.5):
            raise Exception('Dangerously low to ground. Movement aborted')
        # other checks?

        duration = distance / self.DEFAULT_VELOCITY
        send_global_velocity(0, 0, -1 * DEFAULT_VELOCITY, duration)

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


