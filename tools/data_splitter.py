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

    use_rtg: bool, default=True
        Whether to use the real time grapher or not.

    version: 2 / 3, default=2
        Version of python to create rtg subprocess in. Not used if use_rtg=False.
        Currently only tested in 2.7, TCL issues come up w/ 3.6! Use 2.7.
    """

    def __init__(self, logger_desired_headers=[], use_rtg=True, version=2):

        if logger_desired_headers is [] or not logger_desired_headers:
            logging.warning("Splitter: No desired headers for logger!!!")
            logging.critical("Splitter: Logger disabled")
            self.logger = None
        else:
            self.logger = Logger(logger_desired_headers)

        if not use_rtg:
            logging.warning("Splitter: RTG Disabled!")
            self.ipc = None
        else:
            self.ipc = IPC(version=version)

    @property
    def tools_active(self):
        """
        Returns all active tool objects.
        """

        tools_active = []

        if self.logger:
            tools_active.append(self.logger)

        if self.ipc:
            tools_active.append(self.ipc)

        return tools_active

    def exit(self):
        """
        Safely close all created tools.
        """

        logging.warning("Splitter: Exiting all tools...")

        if self.logger:
            self.logger.exit()

        if self.ipc:
            self.ipc.quit()

        logging.warning("Splitter: Successfully exited.")

    def send(self, data):
        """
        Send data everywhere.

        Parameters
        ----------
        data: dict {header: value}
            Data to dispatch.
        """

        if self.logger:
            self.logger.update(data)

        if self.ipc:
            if self.ipc.alive:
                self.ipc.send(data)
            else:
                logging.critical("Splitter: IPC Dead! Removing.")
                self.ipc.quit()
                self.ipc = None


if __name__ == '__main__':
    # Unit test

    import math

    time_to_run = 10  # int(input("How long to log in seconds? "))

    # demo = DataSplitter(use_rtg=False)  # No tools

    # demo = DataSplitter([], use_rtg=True, version=2)  # No logger

    # demo = DataSplitter(['pitch', 'altitude', 'roll', 'yaw', 'voltage'], use_rtg=False)  # No rtg

    demo = DataSplitter(['pitch', 'altitude', 'roll', 'yaw', 'voltage'], use_rtg=True, version=2)  # Both tools

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

        if not demo.tools_active:
            logging.warning("Splitter: Demo: No tools active!")
            break

    demo.exit()
