from tools.real_time_graphing.real_time_graphing import RealTimeGraph

import threading
from multiprocessing import Queue

from time import sleep


class DemoRTGController:
    def __init__(self):
        # TODO - Currently the thread system in rtg seems to be breaking dis

        self.data = Queue()

        self.graph = None

    def create_graph(self):
        self.graph = RealTimeGraph(get_data=self.get_data)

    def send(self, data):
        self.data.put(data)

    def get_data(self):
        return self.data.get()


if __name__ == '__main__':
    # Demo code
    graph = DemoRTGController()

    sleep_time = 1e-2

    def send_data(x):
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

    #
    # Threading stuff
    thread_stop = threading.Event()

    thread_queue = Queue()

    threads = {
        'sender': threading.Thread(target=send_data, args=(thread_queue,)),
        'graph': threading.Thread(target=graph.create_graph)
    }

    for thread in threads.values():
        thread.start()


def stop():
    thread_stop.set()

    for thread in threads.values():
        thread.join()

