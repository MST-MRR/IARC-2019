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
# Takes off to 1 meter, moves forwards 2 meters, right 2 meters, '
# backwards 2 meters , and left two meters (square). At each change
# of direction, the drone hovers for 2 seconds. After completing
# the square, the drone hovers for 5 seconds, and then lands.

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

# Normally a new item would be pushed onto instruction queue when the instruction
# is recevied over the network from the swarm controller
heapq.heappush(controller.instructionQueue, (0, MovementInstruction(2, 0, 0)))
heapq.heappush(controller.instructionQueue, (0, MovementInstruction(0, 2, 0)))
heapq.heappush(controller.instructionQueue, (0, MovementInstruction(-2, 0, 0)))
heapq.heappush(controller.instructionQueue, (0, MovementInstruction(0, -2, 0)))

controller.readNextInstruction()
controller.readNextInstruction()
controller.readNextInstruction()
controller.readNextInstruction()

print("Moving in a square")
while(controller.update()):
    print("Reached vertex, sleeping 2 seconds.")
    time.sleep(2)
    print("Moving to next vertex (unless we are done)")
    

print("Sleeping for 5 seconds...")
time.sleep(10)
print("Done sleeping.")

print("Landing...")
controller.landAndTerminate()
print("Landed!")