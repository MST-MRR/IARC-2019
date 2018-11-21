from pexpect import popen_spawn
import pexpect

try:
    from tools.ipc.data_splitter import DataSplitter
except ImportError:
    from data_splitter import DataSplitter


class IPC:
    def __init__(self):
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
