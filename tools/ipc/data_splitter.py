import threading
from time import time, sleep

try:
    from tools.logging.logger import Logger
except ImportError:
    try:
        from logger import Logger
    except ImportError:
        print("Could not import logger!")

try:
    from tools.real_time_graphing.real_time_graphing import RealTimeGraph
except ImportError:
    try:
        from real_time_graphing import RealTimeGraph
    except ImportError:
        print("Could not import real time grapher!")


class DataSplitter:
    """
    Send data to this one object and it will send to both the RTG and logger

    Parameters
    ----------
    logger_desired_data: dict, default=None
        Parameter of desired data streams for logger object.

    rtg: RealTimeGraph, default=None
        The RealTimeGraph to plot data to if desired.
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

        Parameters
        ----------
        data: dict
            Data to send to rtg and or logger
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
    import ast
    # unit_test()

    def get_data(rtg, thread_stop):
        splitter = DataSplitter(rtg=rtg)

        last_time = this_time = time()
        eof_count = 0

        while last_time + 60 > this_time and eof_count < 15:
            try:
                # TODO - Data gets sent once and then this keeps throwing EOF erros when nothing is trying to be sent
                # TODO - Make break after so many consecutive EOF errors
                # Python 3 uses utf-8 encoding
                inputt = ""
                inputt = input()

                if inputt == "": continue

                print(type(inputt), inputt)

                if type(inputt) is str:
                    data = ast.literal_eval(inputt)
                elif type(inputt) is dict:
                    data = inputt
                else:
                    print("Splitter: Input type: {}, Input: {}".format(type(inputt), inputt))

                print(type(data), data)

                splitter.send(data)

                eof_count = 0
            except EOFError as e:
                # No data came in
                print(e)
                eof_count += 1

            last_time = this_time
            this_time = time()

            if thread_stop.is_set(): break

        print("Splitter: Done getting data!")

    thread_stop = threading.Event()

    rtg = RealTimeGraph(thread_stop=thread_stop)

    threads = {
        'graph': threading.Thread(target=get_data, args=(rtg, thread_stop,))
    }

    for thread in threads.values():
        thread.start()

    rtg.run()  # RTG needs to be in main thread

    thread_stop.set()

    for thread in threads.values():
        thread.join()
