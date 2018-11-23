try:
    from tools.logging.logger import Logger
except ImportError:
    try:
        from logger import Logger
    except ImportError:
        print("Could not import logger!")


class DataSplitter:
    """
    Send data to this one object and it will send to both the RTG and logger
    """

    def __init__(self, logger_desired_data=None, rtg=None):
        self.data = None
        self.rtg = None

        try:
            self.logger = Logger(logger_desired_data)
        except NameError as e:
            print("Failed to create logger object. {}".format(e))
            self.logger = None

        try:
            self.rtg = rtg
            self.rtg.set_pull_function(self.pull)
        except Exception as e:
            print("Failed to create real time graph object. {}".format(e))
            self.rtg = None

    def send(self, data):
        """
        Sends data to tools.
        """

        self.data = data  # Store data for rtg
        if self.logger: self.logger.update(data)  # Send data to logger immediately

    def pull(self):
        """
        Pull stored data
        """

        return self.data


def main(rtg):
    demo = DataSplitter(rtg=rtg)

    for i in range(100000):
        demo.send({
            'altitude': sin(i),
            'airspeed': cos(i),
            'velocity_x': sin(i),
            'velocity_y': cos(i),
            'velocity_z': sin(i),
            'voltage': cos(i),
            'roll': cos(i),
            'pitch': sin(i),
            'yaw': cos(i),
            'target_altitude': sin(i),
            'target_pitch_velocity': cos(i),
            'target_roll_velocity': cos(i),
            'target_yaw': sin(i)
        })


if __name__ == '__main__':
    try:
        from tools.real_time_graphing.real_time_graphing import RealTimeGraph
    except ImportError:
        try:
            from real_time_graphing import RealTimeGraph
        except ImportError:
            print("Could not import real time grapher!")

    import threading
    from queue import Queue
    from time import sleep

    from math import sin, cos

    thread_stop = threading.Event()

    thread_queue = Queue()

    rtg = RealTimeGraph(thread_stop=thread_stop)

    threads = {
        'sender': threading.Thread(target=rtg.run),
        'graph': threading.Thread(target=main, args=(rtg,))
    }

    for thread in threads.values():
        thread.start()

    while not thread_stop.is_set():  # Arbitrary loop for while program is working
        sleep(1)

    for thread in threads.values():
        thread.join()

    rtg = RealTimeGraph



