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
    from tools.interprocess_communication import IPC
except ImportError:
    try:
        from interprocess_communication import IPC
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
            self.ipc = IPC()

    def exit(self):
        """
        Safely close all created objects
        """

        if self.logger:
            self.logger.exit()

        if self.ipc:
            self.ipc.quit()

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
            self.ipc.send(data)


if __name__ == '__main__':
    # Unit test

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
