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


def unit_test():
    def demo_data(rtg, thread_stop):
        demo = DataSplitter(rtg=rtg)

        for i in range(1000):
            demo.send({
                'altitude': sin(i),
                'airspeed': cos(i),
                'velocity_x': sin(i),
                'velocity_y': cos(i),
                'velocity_z': sin(i),
                'voltage': cos(i),
                'roll': cos(i),
                'pitch': 2 * sin(i),
                'yaw': cos(i),
                'target_altitude': sin(i),
                'target_pitch_velocity': cos(i),
                'target_roll_velocity': cos(i),
                'target_yaw': sin(i)
            })
            sleep(.1)

            if thread_stop.is_set(): break

    try:
        from tools.real_time_graphing.real_time_graphing import RealTimeGraph
    except ImportError:
        try:
            from real_time_graphing import RealTimeGraph
        except ImportError:
            print("Could not import real time grapher!")

    import threading
    from time import sleep

    from math import sin, cos

    thread_stop = threading.Event()

    rtg = RealTimeGraph(thread_stop=thread_stop)

    threads = {
        'graph': threading.Thread(target=demo_data, args=(rtg, thread_stop,))
    }

    for thread in threads.values():
        thread.start()

    rtg.run()  # RTG needs to be in main thread

    thread_stop.set()

    for thread in threads.values():
        thread.join()


if __name__ == '__main__':
    unit_test()
