import dronekit
import time
import math
import os
from pymavlink import mavutil
from dronekit import VehicleMode

# Constants
MAINTAIN_ALTITUDE_THRUST = 0.5
DEFAULT_TAKEOFF_THRUST = 0.7
SMOOTH_TAKEOFF_THRUST = 0.6


def connect():
    # Connect to the drone -- TODO: Put in its own function
    return dronekit.connect("tcp:127.0.0.1:5762", wait_ready=True)
    print("\n Connected")

def arm(vehicle):
    while not vehicle.is_armable:
        print("Waiting...\n")
        time.sleep(1.0)

    print("Arming motors\n")
    vehicle.mode = VehicleMode("GUIDED_NOGPS")
    
    while not vehicle.armed:
        vehicle.armed = True
        print("Waiting till armed")
        time.sleep(1)

def test_flight():
    ''' This is a generic flight testing function that does something.
    '''
    vehicle = connect()
    arm(vehicle)

    print("Taking off")
    aTargetAltitude = 1
    thrust = DEFAULT_TAKEOFF_THRUST


    # Here is the Main Loop
    while True:
        current_altitude = vehicle.location.global_relative_frame.alt # Get the drone's current altitude
        print(" Altitude: %f  Desired: %f" % (current_altitude, aTargetAltitude))

        if current_altitude >= aTargetAltitude*0.95: # Trigger just below target alt.
            print("Reached target altitude")
            thrust = 0.5
            break
        elif current_altitude >= aTargetAltitude*0.6:
            thrust = SMOOTH_TAKEOFF_THRUST
        set_attitude(vehicle, roll_angle = -5, thrust = thrust)
        time.sleep(0.2)

    vehicle.VehicleMode = VehicleMode("LAND") 

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

test_flight()
