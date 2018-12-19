import os
import logging

import subprocess
import threading
from time import sleep


class IPC:
    """
    Takes data given to it and sends it to the rtg_cache running in python 3.6
    Python 3 must be able to be run from IPC.py3command's command

    Version: python 2.7

    Parameters
    ----------
    reader: bool, default=True
        Whether or not to use the shell reader.

    thread_stop: threading.Event, default=threading.Event
        The thread stop to be used by shell reader, can pass in own thread stop or allow it to create its own.
    """

    py3command = 'python3'  # Command to start specifically python3 (rename python.exe in Python3 folder to python3.exe)

    def __init__(self, reader=True, thread_stop=threading.Event()):
        self.thread_stop = thread_stop

        self.reader_thread = threading.Thread(target=self.shell_reader)

        filename = 'rtg_cache.py'
        if 'tools' in os.listdir("."):
            filename = 'tools/{}'.format(filename)

        try:
            if reader:
                self.splitter = subprocess.Popen('{} {}'.format(IPC.py3command, filename), stdin=subprocess.PIPE,
                                                 stdout=subprocess.PIPE)
            else:
                self.splitter = subprocess.Popen('{} {}'.format(IPC.py3command, filename), stdin=subprocess.PIPE)

            sleep(.1)  # Give time to start / fail to start

            if self.splitter.poll():
                output, error_output = self.splitter.communicate()
                logging.warning(error_output)

        except Exception as e:
            logging.error("IPC: {}".format(e))
            raise IOError("IPC: Rtg cache file not found!")

        if reader:
            self.start_reader()

    def __enter__(self):
        """
        On enter with statement
        """

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        On exit with statement
        """

        self.quit()

    @property
    def alive(self):
        """
        Returns true if the process is still alive
        """

        return demo.splitter.poll() is None and not self.thread_stop.is_set()

    def quit(self):
        """
        Terminates subprocess and created thread
        """

        logging.info("IPC: Quitting.")
        demo.splitter.terminate()

        self.thread_stop.set()

        try:
            self.reader_thread.join()
        except RuntimeError:
            pass

    def send(self, data):
        """
        Send data to splitter

        Parameters
        ----------
        data:
            Data in format rtg and or logger can read
        """

        if self.splitter.poll() is None:
            try:
                self.splitter.stdin.write("{}\n".format(str(data).encode()))
            except IOError as e:
                logging.warning(e)

            logging.debug("IPC: {}".format(str(data)))
        else:
            logging.error("IPC: Cannot send data")

    def start_reader(self):
        """
        Starts the thread for shell_reader to execute
        """

        self.reader_thread.start()

    def shell_reader(self):
        """
        Reads output from generated subprocess shell
        """

        while not self.thread_stop.is_set():
            out = self.splitter.stdout.readline().strip()  # output w/out \n
            if not out == "":
                print(out)  # Just printing out, let other process choose what to output


if __name__ == '__main__':
    from math import sin, cos

    log_lvl = logging.INFO

    """
    if options.log_level:
        printer = logging.getLogger()
        printer.setLevel(options.log_level)
        handler = logging.StreamHandler()
        handler.setLevel(options.log_level)
        printer.addHandler(handler)
    """

    logging.basicConfig(level=log_lvl)

    with IPC(log_level=log_lvl) as demo:
        for j in range(0, 10000, 3):
            i = j * 1
            demo.send({
                'airspeed': cos(i),
                'velocity_x': sin(i),
                'velocity_y': cos(i),
                'velocity_z': sin(i),
                'altitude': sin(i),
                'target_altitude': sin(i),
                'roll': cos(i),
                'pitch': sin(i),
                'yaw': cos(i),
                'target_roll_velocity': cos(i),
                'target_pitch_velocity': cos(i),
                'target_yaw': sin(i),
                'voltage': cos(i)
            })

            sleep(.1)

            if not demo.alive:
                logging.info("IPC: splitter.poll(): {}".format(demo.splitter.poll()))
                break
