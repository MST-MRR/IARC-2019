import dronekit
import time
import math
import os
from pymavlink import mavutil
from dronekit import VehicleMode
import threading
import temp_rtg_controller
import matplotlib


# Constants
MAINTAIN_ALTITUDE_THRUST = 0.5
DEFAULT_TAKEOFF_THRUST = 0.7
SMOOTH_TAKEOFF_THRUST = 0.6


def connect():
    # Connect to the drone
    return dronekit.connect("tcp:127.0.0.1:5762", wait_ready=True)
    print("\n Connected")

def arm(vehicle):
    while not vehicle.is_armable:
        print("Waiting...\n")
        time.sleep(1.0)

    print("Arming motors\n")
    vehicle.mode = VehicleMode("GUIDED")

    while not vehicle.armed:
        vehicle.armed = True
        print("Waiting till armed")
        time.sleep(1)

def test_flight(vehicle):
    ''' This is a generic flight testing function that does something.
    '''
    print("Taking off")
    arm_and_takeoff_nogps(vehicle, 2)

    print("Hold for 15 seconds")
    set_attitude(vehicle, duration = 15)
    #print("IMPORTANT~~~~~~~~~~~~~~~~")
    #print(vehicle.location.local_frame)
    #print("Move a little for 10 seconds")
    #set_attitude(vehicle, roll_angle=-1, duration=10)

    #print("Move a little back for 10 seconds")
    #set_attitude(vehicle, roll_angle=1, duration=10)
    
    print("Landing")
    while (not vehicle.mode == VehicleMode("LAND")):
        vehicle.mode = VehicleMode("LAND")

    return True

def print_info(threadName, vehicle, exitflag):
    while exitflag:
        print("VEHICLE ALTITUDE: ", vehicle.location.global_relative_frame.alt)
        print "Attitude: %s" % vehicle.attitude
        print "Velocity: %s" % vehicle.velocity
        time.sleep(1)

def set_attitude(vehicle, roll_angle = 0.0, pitch_angle = 0.0, yaw_rate = 0.0, thrust = 0.5, duration = 0):
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
    msg = vehicle.message_factory.set_attitude_target_encode(
        0, # time_boot_ms
        1, # Target system
        1, # Target component
        0b00000000, # Type mask: bit 1 is LSB
        to_quaternion(roll_angle, pitch_angle), # Quaternion
        0, # Body roll rate in radian
        0, # Body pitch rate in radian
        math.radians(yaw_rate), # Body yaw rate in radian
        thrust  # Thrust
    )
    vehicle.send_mavlink(msg)

    start = time.time()
    while time.time() - start < duration:
        vehicle.send_mavlink(msg)
        time.sleep(0.1)

def to_quaternion(roll = 0.0, pitch = 0.0, yaw = 0.0):
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


def arm_and_takeoff_nogps(vehicle, aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude without GPS data.
    """

    ##### CONSTANTS #####
    DEFAULT_TAKEOFF_THRUST = 0.7
    SMOOTH_TAKEOFF_THRUST = 0.6

    print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    # If you need to disable the arming check,
    # just comment it with your own responsibility.
    '''
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)
    '''

    print("Arming motors")
    # Copter should arm in GUIDED_NOGPS mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        vehicle.armed = True
        time.sleep(1)

    print("Taking off!")

    thrust = DEFAULT_TAKEOFF_THRUST
    while True:
        current_altitude = vehicle.location.global_relative_frame.alt
        print(" Altitude: %f  Desired: %f" %
              (current_altitude, aTargetAltitude))
        if current_altitude >= aTargetAltitude*0.95: # Trigger just below target alt.
            print("Reached target altitude")
            break
        elif current_altitude >= aTargetAltitude*0.6:
            thrust = SMOOTH_TAKEOFF_THRUST
        set_attitude(vehicle, thrust = thrust)
        time.sleep(0.2)

def get_info():
    return {'roll':5 ,'pitch':7}

def send_global_velocity(velocity_x, velocity_y, velocity_z, duration, vehicle):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_global_int_encode(
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
        vehicle.send_mavlink(msg)
        time.sleep(1)

class infoThread (threading.Thread):
    def __init__(self, threadID, name, vehicle):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.vehicle = vehicle
        self.exitflag = True
    def run(self):
      print "Starting " + self.name
      print_info(self.name, self.vehicle, self.exitflag)
      print "Exiting " + self.name
    def stop(self):
        self.exitflag = False

class testThread(threading.Thread):
    def __init__(self, threadID, name, vehicle):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.vehicle = vehicle
        self.status = False
    def run(self):
        self.status = test_flight(vehicle)


vehicle = connect()
thread_stop = threading.Event()
graph1 = temp_rtg_controller.DemoRTGController()
graphthread = threading.Thread(target=graph1.create_graph, args=(thread_stop,))
#thread1 = infoThread(1, "Thread-1", vehicle)
#thread1.start()
thread2 = testThread(2, "Thread-2" , vehicle)
thread2.start()
while True:
    try:
        if thread2.status:
            #thread1.stop()
            break;
    except KeyboardInterrupt:
        break;