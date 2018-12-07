import logging
from time import time, sleep

import sys
import threading

try:
    from tools.logger import Logger
except ImportError:
    try:
        from logger import Logger
    except ImportError as e:
        logging.error(e)

try:
    from tools.real_time_graphing import RealTimeGraph
except ImportError:
    try:
        from real_time_graphing import RealTimeGraph
    except ImportError as e:
        logging.error(e)


class DataSplitter:
    """
    Send data to this one object and it will send to both the RTG and logger

    Version: python 3.6

    Parameters
    ----------
    log_level: logging.LEVEL, default=None
        If logging is desired set a logging level.

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
            logging.warning("Failed to create logger object. {}".format(e))
            self.logger = None

        if rtg:
            self.rtg = rtg
            self.rtg.set_pull_function(self.pull)

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


def unit_test(rtg, thread_stop):
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

    if rtg:
        threads = {
            'graph': threading.Thread(target=demo_data, args=(rtg, thread_stop,))
        }

        for thread in threads.values():
            thread.start()

        rtg.run()  # RTG needs to be in main thread

        thread_stop.set()

        for thread in threads.values():
            thread.join()
    else:
        demo_data(rtg, thread_stop)


def get_data(rtg, thread_stop):
    splitter = DataSplitter(rtg=rtg)

    logging.info("Splitter: Starting...")

    last_time = this_time = time()
    eof_count = 0

    while last_time + 15 > this_time:
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
    import ast  # to interpret input

    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument("-d", "--debug", type=bool, nargs='?', dest="debug", default=False,
                        help="To use or not to use debug mode.")

    parser.add_argument("-l", "--log-level", type=int, nargs='?', dest="log_level", default=30,
                        help="What logging level to use.")

    options = parser.parse_args()

    thread_stop = threading.Event()

    if options.log_level:
        printer = logging.getLogger()
        printer.setLevel(options.log_level)
        handler = logging.StreamHandler()
        handler.setLevel(options.log_level)
        printer.addHandler(handler)

    try:
        rtg = RealTimeGraph(thread_stop=thread_stop)
    except NameError as e:
        logging.warning(e)
        rtg = None

    if options.debug:
        unit_test(rtg, thread_stop)
    else:
        if rtg:
            getter_thread = threading.Thread(target=get_data, args=(rtg, thread_stop,))

            getter_thread.start()

            rtg.run()  # RTG needs to be in main thread

            thread_stop.set()

            getter_thread.join()
        else:
            get_data(rtg, thread_stop)
