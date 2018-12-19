import logging
from time import time, sleep

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
    Send data to this and it will send to both the logger & IPC(RTG)

    Version: python 2.7

    Parameters
    ----------
    logger_desired_headers: list, default=[]
        Headers for logger to log data for. Logger object not created if no headers given.

    rtg: bool, default=True
        Whether to use the real time grapher or not
    """

    def __init__(self, logger_desired_headers=[], rtg=True):

        if logger_desired_headers is [] or not logger_desired_headers:
            logging.critical("Splitter: No desired headers for logger!!!")
            self.logger = None
        else:
            self.logger = Logger(logger_desired_headers)

        if not rtg:
            logging.warning("Splitter: RTG Disabled!")
            self.ipc = None
        else:
            # Create ipc
            self.ipc = None               # TODO implement

    def exit(self):
        """
        Safely close all created objects
        """

        if self.logger:
            self.logger.exit()

    def send(self, data):
        """
        Send data everywhere.

        Parameters
        ----------
        data: dict {header: value}
            Data to dispatch
        """

        if self.logger:
            self.logger.update(data)

        if self.ipc:
                        # TODO - self.ipc.send(data)
            pass

"""
def unit_test(rtg, thread_stop):
    from math import sin, cos

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
            received = sys.stdin.readline()  # Python 3 uses utf-8 encoding

            # logging.info("Splitter: Input type: {}, Input: {}".format(type(inputt), inputt))

            if type(received) is str:
                data = ast.literal_eval(received)
            elif type(received) is dict:
                data = received
            else:
                logging.warning("Splitter: Input type: {}, Input: {}".format(type(received), received))

            logging.debug("Splitter: {}".format(data))

            splitter.send(data)

            eof_count = 0
        except EOFError as e:
            # No data came in
            logging.warning("Splitter: {}".format(e))
            eof_count += 1

        last_time = this_time
        this_time = time()

        if thread_stop.is_set(): break

    logging.info("Splitter: Done getting data!")


if __name__ == '__main__':
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
        logging.warning("Splitter: {}".format(e))
        rtg = None

    if options.debug:
        unit_test(rtg, thread_stop)
    else:
        import ast  # For interpreting received data

        if rtg:
            getter_thread = threading.Thread(target=get_data, args=(rtg, thread_stop,))

            getter_thread.start()

            rtg.run()  # RTG needs to be in main thread

            thread_stop.set()

            getter_thread.join()
        else:
            get_data(rtg=None, thread_stop=thread_stop)
"""

if __name__ == '__main__':
    # Unit test

    # TODO - Test rtg wanting data not getting it

    import math

    time_to_run = int(input("How long to log in seconds? "))

    demo = DataSplitter(['airspeed', 'altitude', 'pitch', 'roll', 'yaw', 'velocity_x',
                         'velocity_y', 'velocity_z', 'voltage'], False)

    start_time = time()
    time_elapsed = 0

    def func(x):
        return math.cos(x)

    while time_elapsed < time_to_run:
        myData = {
            'airspeed': func(time_elapsed) + .0,
            'altitude': func(time_elapsed) + .1,
            'pitch': func(time_elapsed) + .2,
            'roll': func(time_elapsed) + .3,
            # 'yaw' : func(time_elapsed) + .4,
            'velocity_x': func(time_elapsed) + .5,
            'velocity_y': func(time_elapsed) + .6,
            'velocity_z': func(time_elapsed) + .7,
            'voltage': func(time_elapsed) + .8
        }

        demo.send(myData)

        time_elapsed = time() - start_time

        sleep(.00001)

    demo.exit()
