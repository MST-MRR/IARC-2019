import os
import logging

import subprocess
import threading
from time import sleep


class IPC:
    """
    Creates subprocess in python 2.7 or 3.6 that it can send and receive data from.

    Currently have TCL problems in 3.6 w/ data_splitter! Use 2.7.

    Version: python 2.7

    Parameters
    ----------
    version: 2/3, default=2
        Version of python to create subprocess in.
        Only tested w/ data splitter in 2.7!

    reader: bool, default=True
        Whether or not to use the shell reader.

    thread_stop: threading.Event, default=threading.Event
        The thread stop to be used by shell reader, pass in own thread stop or allow it to create its own.
    """

    py2command = 'python'  # Command to start python 2.7
    py3command = 'python3'  # Command to start python 3.6 (rename python.exe in Python3 folder to python3.exe)

    def __init__(self, version=2, reader=True, thread_stop=threading.Event()):
        self.thread_stop = thread_stop

        # Get filename

        filename = 'rtg_cache.py'
        if 'tools' in os.listdir("."):
            filename = 'tools/{}'.format(filename)

        # Set python command
        python_command = IPC.py3command if version != 2 else IPC.py2command

        # Start subprocess

        try:
            # Attempt start

            if reader:
                self.subprocess = subprocess.Popen('{} {}'.format(python_command, filename), stdin=subprocess.PIPE,
                                                   stdout=subprocess.PIPE)
            else:
                self.subprocess = subprocess.Popen('{} {}'.format(python_command, filename), stdin=subprocess.PIPE)

            sleep(.1)  # Give time to start / fail to start

            # See if started

            if self.subprocess.poll():
                output, error_output = self.subprocess.communicate()
                logging.warning("IPC: Poll: {}".format(error_output))

        except Exception as e:
            logging.error("IPC: {}".format(e))
            raise IOError("IPC: Rtg cache file not found!")

        # Shell reader

        if reader:
            self.reader_thread = threading.Thread(target=self.continuous_shell_reader)
            self.reader_thread.start()

    def __enter__(self):
        """
        On enter with statement.
        """

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        On exit with statement.
        """

        self.quit()

    @property
    def alive(self):
        """
        If process is still alive or not.
        """

        return self.subprocess.poll() is None and not self.thread_stop.is_set()

    def quit(self):
        """
        Terminates subprocess and created thread.
        """

        logging.warning("IPC: Quitting.")
        self.subprocess.terminate()

        self.thread_stop.set()

        try:
            self.reader_thread.join()
        except RuntimeError:
            pass

    def send(self, data):
        """
        Send data to subprocess.

        Parameters
        ----------
        data:
            Data in format subprocess can read.
        """

        if self.subprocess.poll() is None:
            try:
                self.subprocess.stdin.write("{}\n".format(str(data).encode()))
            except IOError as e:
                logging.warning("IPC: Failed to send data! IOError: {}".format(e))

            logging.debug("IPC: {}".format(str(data)))
        else:
            logging.error("IPC: Process is dead! Poll: {}".format(self.subprocess.poll()))

    def shell_reader(self):
        """
        Returns output from generated subprocess shell.
        """

        return self.subprocess.stdout.readline().strip()  # output w/out \n

    def continuous_shell_reader(self):
        """
        Continuously read output form subprocess shell
        """

        while not self.thread_stop.is_set():
            out = self.shell_reader()

            if not out == "":
                print("IPC: Received: {}".format(out))


if __name__ == '__main__':
    from math import sin, cos

    logging.basicConfig(level=logging.INFO)

    with IPC(version=2) as demo:
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
                logging.info("IPC: splitter.poll(): {}".format(demo.subprocess.poll()))
                break
