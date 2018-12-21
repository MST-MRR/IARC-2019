
import time
import sys
import os
import heapq # temporary (we want to implement our own)
import threading

from ..Drone.drone import Drone
from ..Drone.drone_controller import DroneController
from ..Instructions.Movement.movement_instruction import MovementInstruction
from ..Utilities import safety_checks
from ..tools import logger
from ..tools.ipc.interprocess_communication import IPC


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

    emergency_land_event = safety_checks.init_emergency_land_event()

    controller = DroneController(Drone(), emergency_land_event)

    if do_tools:
        import threading

        data_sender = IPC()

        thread_stop = threading.Event()

        threads = {
            'tools': threading.Thread(target=send_data, args=(data_sender, controller.drone.vehicle, thread_stop,))
        }

        for thread in threads.values():
            thread.start()

    #lgger = lo  # Caused error

    controller.start()

    safety_checks.start_safety_loop(emergency_land_event)

    if do_tools:
        thread_stop.set()

        for thread in threads.values():
            thread.join()