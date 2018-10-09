import dronekit
import time
import math
from Periodic import Periodic
from pymavlink import mavutil

vehicle = None
enabled = False
real = False

def periodic():
    global enabled
    startTime = time.time()
    flightStep = 0
    '''#Move based on previous location
    while enabled:
        if (flightStep == 0):
            Periodic.fly(6.0, 0.0, 6.0)
        elif (flightStep == 1):
            Periodic.fly(0.0, 6.0, 3.0)
        elif (flightStep == 2):
            Periodic.fly(-6.0, 0.0, 6.0)
        elif (flightStep == 3):
            Periodic.fly(0.0, -6.0, 3.0)
        elif (flightStep == 4):
            enabled = False
        currentTime = time.time()
        #print vehicle.velocity
        if (currentTime - startTime > 10):
            flightStep+=1
            Periodic.resetLocation()
            startTime = currentTime
            '''

    #Move based on starting location
    while enabled:
        if (flightStep == 0):
            Periodic.fly(0.0, 0.0, 5.0)
        elif (flightStep == 1):
            Periodic.fly(6.0, 6.0, 2.0)
        elif (flightStep == 2):
            Periodic.fly(0.0, 6.0, 5.0)
        elif (flightStep == 3):
            Periodic.fly(0.0, 0.0, 2.0)
        elif (flightStep == 4):
            enabled = False
        currentTime = time.time()
        #if (currentTime - startTime > 8):
        #    flightStep+=1
        #    startTime = currentTime
        if (Periodic.stepComplete):
            flightStep += 1

def main():
    global enabled
    global vehicle
    global real
    connect()

    arm()

    print "Taking off"
    takeoffAlt = 3

    vehicle.simple_takeoff(takeoffAlt)

    while True:
        #print vehicle.mode
        #print vehicle.armed
        if (not real):
            altitude = vehicle.location.global_relative_frame.alt
        else:
            altitude = vehicle.rangefinder.distance
        print " Altitude: ", altitude
        # Break and return from function just below target altitude.
        #Periodic.fly(0.0, 0.0, takeoffAlt)
        #Periodic.send_ned_velocity(0.0, 0.0, 0.5)

        if altitude >= takeoffAlt * 0.94:
            print "Reached target altitude"
            break
        time.sleep(0.5)
    print "Takeoff complete"

    periodic()

    print "Landing"
    while (altitude > 0.03):
        vehicle.mode = dronekit.VehicleMode("LAND")
    time.sleep(8)

def connect():
    global vehicle
    global real

    if (not real):
        vehicle = dronekit.connect('tcp:127.0.0.1:5762', wait_ready=True)  # SITL (Simulator)
    else:
        vehicle = dronekit.connect('/dev/serial/by-id/usb-3D_Robotics_PX4_FMU_v2.x_0-if00', wait_ready=True)
    print "connected"

def arm():
    global enabled
    global vehicle
    enabled = True
    Periodic.init()
    Periodic.setVehicle(vehicle, mavutil.mavlink.MAV_FRAME_LOCAL_NED)
    vehicle.mode = dronekit.VehicleMode("GUIDED")

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    #while not vehicle.is_armable:
        #print " Waiting for vehicle to initialise..."
        #vehicle.armed = True
        #time.sleep(1)

    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print " Waiting for arming..."
        vehicle.armed = True
        time.sleep(1)
    print "Armed!"

main()
