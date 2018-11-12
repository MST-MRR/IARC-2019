from TestDrone import TestDrone
from TestDroneController import TestDroneController
import time
import sys
import os
from MovementInstruction import MovementInstruction
import heapq # temporary

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
heapq.heappush(controller.instructionQueue, (0, MovementInstruction(-2, 2, 0)))

controller.readNextInstruction()
controller.readNextInstruction()

print(controller.movementQueue)

while(controller.update()):
    pass

print("Landing...")
controller.landAndTerminate()
print("Landed!")

# Working test code (does not use drone controller instance)
"""
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
"""
