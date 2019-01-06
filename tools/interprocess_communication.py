import os
import logging

import shlex
import subprocess
import threading
from time import sleep


class IPC:
    """
    Creates subprocess in python 2.7 that it can send and receive data from.

    Version: python 2.7

    Parameters
    ----------
    reader: bool, default=True
        Whether or not to use the shell reader.

    thread_stop: threading.Event, default=threading.Event
        The thread stop to be used by shell reader, pass in own thread stop or allow it to create its own.
    """

    python_command = 'python'  # Command to start python 2.7

    working_filename = 'interprocess_communication.py'  # The name of this file

    target_path = "rtg_cache.py"  # Relative path to target file

    def __init__(self, reader=True, thread_stop=threading.Event()):
        self.thread_stop = thread_stop

        # Get filename

        filename = __file__.split(IPC.working_filename)[0]  # Get this files location

        if filename[-1] not in ["\\", "/"]:
            filename += '/'
        
        filename += IPC.target_path

        # Start subprocess

        try:
            # Attempt start

            if reader:
                self.subprocess = subprocess.Popen(shlex.split('{} {}'.format(IPC.python_command, filename)), stdin=subprocess.PIPE,
                                                   stdout=subprocess.PIPE)
            else:
                self.subprocess = subprocess.Popen(shlex.split('{} {}'.format(IPC.python_command, filename)), stdin=subprocess.PIPE)

            sleep(.1)  # Give time to start / fail to start

            # See if started

            if self.subprocess.poll():
                output, error_output = self.subprocess.communicate()
                logging.warning("IPC: Poll: {}".format(error_output))

        except Exception as e:
            raise IOError("IPC: {}".format(e))

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
        try:
          self.subprocess.terminate()
        except OSError:
            pass
          
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

    with IPC() as demo:
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
