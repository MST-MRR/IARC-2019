import sys
sys.path.insert(0, '..')

from TestDrone import TestDrone
from TestDroneController import TestDroneController
import time
import sys
import os
from MovementInstruction import MovementInstruction
import heapq # temporary

# MISSION DESCRIPTION:
# Takes off to 1 meter, hovers for 10 seconds, and then lands.

# This test uses a drone controller
controller = TestDroneController()

# Get the controller ready
controller.setId()
controller.setDrone()
controller.drone.connect(isInSimulator = True)
controller.drone.arm()

print("Taking off...")
controller.takeoff(1)
print("Take off complete!")

print("Sleeping for 10 seconds...")
time.sleep(10)
print("Done sleeping.")

print("Landing...")
controller.landAndTerminate()
print("Landed!")