from TestDrone import TestDrone
import time

drone = TestDrone()

drone.connect()
print("Connected!")

drone.arm()
print("Armed!")

try:
    print("Taking off...")
    drone.takeoff()
    print("Take off complete!")

    # Move in a square (these kinds of command normally would be called by a drone controller)
    drone.forward(5)
    drone.right(5)
    drone.backward(5)
    drone.left(5)

    print("Landing...")
    drone.land()
    print("Landed!")

except Exception as error:
    print("Error encountered:", error)
    print("Emergency landing!")
    drone.land()

print("Mission terminated.")
