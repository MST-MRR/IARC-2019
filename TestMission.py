from TestDrone import TestDrone
import time
import sys
import os

drone = TestDrone()

print("Connecting...")
drone.connect()
print("Connected!")

drone.arm()
print("Armed!")

try:
    print("Taking off...")
    drone.takeoff(5)
    print("Take off complete!")

    # Move in a square (these kinds of command normally would be called by a drone controller)
    drone.forward(distance = 5)
    drone.right(distance = 5)
    drone.backward(distance = 5)
    drone.left(distance = 5)

    print("Landing...")
    drone.land()
    print("Landed!")

except Exception as error:
    print("Error encountered:", error)
    print("Emergency landing!")
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    drone.land()

print("Mission terminated.")
