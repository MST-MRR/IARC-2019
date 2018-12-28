# Standard Library
import heapq 
import os
import sys
import threading
import time

# Ours
from ..Drone.drone import Drone
from ..Drone.drone_controller import DroneController
from ..Instructions.Movement.movement_instruction import MovementInstruction
from ..tools import logger
from ..tools.ipc.interprocess_communication import IPC
from ..Utilities.emergency_land import EmergencyLand

def send_data(ipc, drone, stop):
    while not stop.is_set():
        try:
            ipc.send({'pitch': drone.pitch, 'roll': drone.roll})
        except AttributeError:
            time.sleep(.5)

        time.sleep(.1)

        if ipc.splitter.poll() is not None:
            print("IPC: splitter.poll(): {}".format(ipc.splitter.poll()))
            break

    print("IPC: Done sending data.")
    ipc.splitter.terminate()


if __name__ == '__main__':
    do_tools = False  # Toggle whether to use logging/rtg

    controller = DroneController()

    if do_tools:

        data_sender = IPC()

        thread_stop = threading.Event()

        threads = {
            'tools': threading.Thread(target=send_data, args=(data_sender, controller.drone.vehicle, thread_stop,))
        }

        for thread in threads.values():
            thread.start()

    #lgger = lo  # Caused error
    
    controller.start()
    
    EmergencyLand.start_safety_net()

    # Would never get here because of the way EmergencyLand is implemented
    # (it doesn't return until is ensures a set number of threads have ended)
    if do_tools:
        thread_stop.set()

        for thread in threads.values():
            thread.join()