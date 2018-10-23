import sys, os

from tools.real_time_graphing.real_time_graphing import RealTimeGraph

import threading
from multiprocessing import Queue

from time import sleep


class DemoRTGController:
    def __init__(self):
        # TODO - Currently the thread system in rtg seems to be breaking dis

        self.data = Queue()

        self.graph = None

    def create_graph(self, thread_stop):
        self.graph = RealTimeGraph(get_data=self.get_data, thread_stop=thread_stop)

    def send(self, data):
        self.data.put(data)

    def get_data(self):
        return self.data.get()


def demo_send_data(graph):
    sleep_time = 1e-2

    # Can get dictionary from tools/real_time_graphing/demo_data_gen
    while not thread_stop.is_set():
        print "sent"
        graph.send({
            'altitude': 1,
            'airspeed': 2,
            'velocity_x': 3,
            'velocity_y': 2,
            'velocity_z': 1,
            'voltage': 2,
            'roll': 3,
            'pitch': 2,
            'yaw': 1,
            'altitude_controller_output': 2,
            'altitude_rc_output': 3,
            'target_altitude': 2,
            'pitch_controller_output': 1,
            'pitch_rc_output': 2,
            'target_pitch_velocity': 3,
            'roll_controller_output': 2,
            'roll_rc_output': 1,
            'target_roll_velocity': 2,
            'yaw_controller_output': 3,
            'yaw_rc_output': 2,
            'target_yaw': 1,
        })

        sleep(sleep_time)


if __name__ == '__main__':
    # Demo code
    graph = DemoRTGController()

    #
    # Threading stuff
    thread_stop = threading.Event()

    thread_queue = Queue()

    threads = {
        'sender': threading.Thread(target=demo_send_data, args=(graph,)),
        'graph': threading.Thread(target=graph.create_graph, args=(thread_stop,))
    }

    for thread in threads.values():
        thread.start()

    while not thread_stop.is_set():  # Arbitrary loop for while program is working
        sleep(1)

    for thread in threads.values():
        thread.join()

    os._exit(0)  # Cannot find another way to make process terminate


