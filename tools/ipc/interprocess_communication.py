import subprocess
import threading
from time import sleep

# TODO - Make sure everything works from multiple start locations

# TODO - ERROR, WARNING, INFO
# TODO - Colorama or logging

# TODO - How to tell whether to use rtg or logger

# TODO - Able to use with statement?


class IPC:
    """
    Takes data sent to it and sends it to the datasplitter running in python 3.6
    Meant to run in python 2.7
    Python 3 must be able to be run from python3 command

    """

    def __init__(self, thread_stop=threading.Event()):
        for filename in ['tools/ipc/data_splitter.py', 'data_splitter.py']:
            self.splitter = subprocess.Popen('python3 {}'.format(filename), stdin=subprocess.PIPE, stdout=subprocess.PIPE)

            sleep(.1)  # Poll will return None(None means process working) if immediately called after creating obj
            if not self.splitter.poll():
                break  # Success!
            else:
                output, error_output = self.splitter.communicate()
                print(error_output)
        else:
            # If loops through file names & doesnt find data splitter
            raise IOError("Data splitter file not found!")
            return

        self.thread_stop = thread_stop

        self.threads = {'output_reader': threading.Thread(target=self.shell_reader)}

        for thread in self.threads.values():
            thread.start()

    def quit(self):
        """
        Terminates subprocess and created thread
        """

        print("IPC: Done sending data.")
        demo.splitter.terminate()

        self.thread_stop.set()

        for thread in self.threads.values():
            thread.join()

    def send(self, data):
        """

        Parameters
        ----------
        data:
            Data in format rtg and or logger can read
        """
        if self.splitter.poll() is None:
            try:
                self.splitter.stdin.write("{}\n".format(str(data).encode()))  # Lots of warnings against stdin!
            except IOError as e:
                print(e)

            print("IPC: {}".format(str(data)))
        else:
            print("IPC: Cannot send data")

    def shell_reader(self):
        """
        Reads output from generated subprocess shell
        """

        while not self.thread_stop.is_set():
            out = self.splitter.stdout.readline().strip()  # output w/out \n
            if not out == "": print(out)


if __name__ == '__main__':

    from math import sin, cos

    demo = IPC()

    for j in range(10000):
        i = j / 3.14
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

        if demo.splitter.poll() is not None or demo.thread_stop.is_set():
            print("IPC: splitter.poll(): {}".format(demo.splitter.poll()))
            break

    demo.quit()

