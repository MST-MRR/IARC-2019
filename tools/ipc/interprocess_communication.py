from pexpect import popen_spawn
import pexpect

try:
    from tools.ipc.data_splitter import DataSplitter
except ImportError:
    from data_splitter import DataSplitter


class IPC:
    def __init__(self):
        # TODO - Create rtg & data splitter in python 3, this class is in python 2 but allow it to send data to splitter
        # TODO - Remember to send rtg to splitter
        # Should be used in python 2.7

        # Different commands for windows and linux
        # TODO - Pass classes in to be used?- > no bc need datasplitter pull function

        # IPC(pexpect) -> Data handler -> Send data to logger and rtg can pass in logger?

        os_windows = True

        pyfile = "../real_time_graphing"

        # Windows version normally just spawn
        if os_windows:
            py3 = popen_spawn.PopenSpawn('python {}'.format(pyfile), timeout=2)
        else:
            py3 = pexpect.spawn('python3 {}'.format(pyfile), timeout=2)

        # Should only be sending data to tools

        # Create data splitter and send it data w/ send(data)

        self.splitter = DataSplitter(desired_data)

    def send(self, data):
        self.splitter.send(data)


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
        'graph': threading.Thread(target=main, args=(rtg, thread_stop,))
    }

    for thread in threads.values():
        thread.start()

    rtg.run()  # RTG needs to be in main thread?

    thread_stop.set()

    for thread in threads.values():
        thread.join()
