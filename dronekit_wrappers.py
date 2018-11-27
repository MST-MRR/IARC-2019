from time import sleep, time
from math import radians, sin, cos
from pymavlink import mavutil
import dronekit
import threading
from sys import stdout

"""
Any functions requiring the use of DroneKit's message_factory module to construct
mavlink commands are stored here.
"""

# Tells the drone to move with the given velocities in the x, y, and z direction
# for a specifies number of seconds.
def send_global_velocity(vehicle, (velocity_x, velocity_y, velocity_z), duration, stop_event):
    """
    Moves vehicle in direction of the give three-dimentional velocity vector for the
    given duration in seconds.  

    Parameters
    ----------
    vehicle: DroneKit.Vehicle
        Interface to the drone
    (velocity_x, velocity_y, velocity_z): (Double, Double, Double)
        Velocity vector to travel along
    duration: Integer
        How long in seconds to fly along vector
    stop_event: threading.Event
        Set whenever the current thread is being canceled

    Precondition:
    ----------
    None

    Postcondition:
    ----------
    None

    Returns:
    ----------
    None
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

    print threading.current_thread().name, "Velocity: (", velocity_x, ", ", velocity_y, ", ", velocity_z, ")"
    print threading.current_thread().name, ": Sending velocity ",
    # send command to vehicle on 1 Hz cycle
    for x in range(0, duration):
        if stop_event.isSet():
            print threading.current_thread().name, ": Movement halting"
            stop_event.clear()
            return
        print ".",
        stdout.flush()
        vehicle.send_mavlink(msg)
        sleep(1)
    print ""

def set_attitude(vehicle, roll_angle = 0.0, pitch_angle = 0.0, yaw_rate = 0.0, thrust = 0.5):
    """
    TODO: give a good description of what this function does

    Parameters
    ----------
    vehicle: DroneKit.Vehicle
        Interface to the drone
    roll_angle: Double (optional)
        TODO
    pitch_angle: Double (optional)
        TODO
    yaw_rate: Double (optional)
        TODO
    thrust: Double (optional)
        TODO

    Precondition:
    ----------
    TODO

    Postcondition:
    ----------
    TODO

    Returns:
    ----------
    None
    
    The follow comments are from the DroneKit website:

    Note that from AC3.3 the message should be re-sent every second (after about 3 seconds
    with no message the velocity will drop back to zero). In AC3.2.1 and earlier the specified
    velocity persists until it is canceled. The code below should work on either version
    (sending the message multiple times does not cause problems).

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
        radians(yaw_rate), # Body yaw rate in radian
        thrust  # Thrust
    )
    vehicle.send_mavlink(msg)

def to_quaternion(roll = 0.0, pitch = 0.0, yaw = 0.0):
    """
    Convert degrees to quaternions

    Parameters
    ----------
    roll: Double (optional)
        TODO
    pitch: Double (optional)
        TODO
    yaw: Double (optional)
        TODO


    Precondition:
    ----------
    TODO

    Postcondition:
    ----------
    TODO
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