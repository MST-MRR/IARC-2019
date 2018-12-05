import logging

import sys
import threading
from time import time, sleep

try:
    from tools.logging.logger import Logger
except ImportError:
    try:
        from logger import Logger
    except ImportError:
        logging.warning("Could not import logger!")

try:
    from tools.real_time_graphing.real_time_graphing import RealTimeGraph
except ImportError:
    try:
        from real_time_graphing import RealTimeGraph
    except ImportError:
        logging.warning("Could not import real time grapher!")


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

    def __init__(self, log_level=None, logger_desired_data=None, rtg=None):
        if log_level:
            printer = logging.getLogger()

            if not printer.handlers:
                printer.setLevel(log_level)
                handler = logging.StreamHandler()
                handler.setLevel(log_level)
                printer.addHandler(handler)

        self.data = None
        self.rtg = None

        try:
            self.logger = Logger(logger_desired_data)
        except NameError as e:
            logging.warning("Failed to create logger object. {}".format(e))
            self.logger = None

        try:
            self.rtg = rtg
            self.rtg.set_pull_function(self.pull)
        except Exception as e:
            logging.warning("Failed to create real time graph object. {}".format(e))
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

        logging.info("Splitter: Starting...")

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


def get_data(rtg, thread_stop):
    splitter = DataSplitter(logging.INFO, rtg=rtg)

    logging.info("Splitter: Starting...")

    last_time = this_time = time()
    eof_count = 0

    while last_time + 15 > this_time and eof_count < 15:
        try:
            # Python 3 uses utf-8 encoding
            inputt = sys.stdin.readline()

            # logging.info("Splitter: Input type: {}, Input: {}".format(type(inputt), inputt))

            if type(inputt) is str:
                data = ast.literal_eval(inputt)
            elif type(inputt) is dict:
                data = inputt
            else:
                logging.warning("Splitter: Input type: {}, Input: {}".format(type(inputt), inputt))

            logging.info("SPLITTER: {}".format(data))

            splitter.send(data)

            eof_count = 0
        except EOFError as e:
            # No data came in
            logging.warning(e)
            eof_count += 1

        last_time = this_time
        this_time = time()

        if thread_stop.is_set(): break

    logging.info("SPLITTER: Done getting data!")


if __name__ == '__main__':
    import ast
    # unit_test()

    thread_stop = threading.Event()

    rtg = RealTimeGraph(thread_stop=thread_stop)

    getter_thread = threading.Thread(target=get_data, args=(rtg, thread_stop,))

    getter_thread.start()

    rtg.run()  # RTG needs to be in main thread

    thread_stop.set()

    getter_thread.join()
