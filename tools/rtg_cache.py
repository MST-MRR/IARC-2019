import logging

import threading
import sys
from ast import literal_eval

from real_time_graphing import RealTimeGraph


class RTGCache:
    """
    Serves as intermediary for IPC and RTG.
    IPC sends when it gets data but this needs to constantly look for that data.
    RTG constantly tries to pull data so it is cached here
    """

    def __init__(self):
        self.data = {}

        self.rtg = RealTimeGraph(get_data=self.pull)

    def start(self):
        """
        Start rtg
        """

        def repeating_read_stdin(stopper):
            while not stopper.is_set():
                self.read_stdin()

        thread_stop = threading.Event()

        getter_thread = threading.Thread(target=repeating_read_stdin, args=(thread_stop,))
        getter_thread.start()

        self.rtg.run()  # Ran in main thread

        thread_stop.set()

        getter_thread.join()

    def pull(self):
        """
        Returns stored data
        """

        return self.data

    def read_stdin(self):
        """
        Read input
        """

        try:
            received = sys.stdin.readline()     # TODO - Make timeout

            # logging.info("Splitter: Input type: {}, Input: {}".format(type(inputt), inputt))

            if type(received) is str:
                data = literal_eval(received)
            elif type(received) is dict:
                data = received
            else:
                logging.warning("Cache: Input type unexpected! Type: {}, Raw: {}".format(type(received), received))

            logging.debug("Cache: Received: {}".format(data))

            self.data = data

        except EOFError as e:
            logging.warning("Cache: Data not received! {}".format(e))


if __name__ == '__main__':
    """
    # Unit test

    from real_time_graph.demo_data_gen import get_demo_data

    demo = RTGCache()

    demo.data = get_demo_data()  # Only for unit test

    demo.start()
    """

    # Main

    cache = RTGCache()
    cache.start()
