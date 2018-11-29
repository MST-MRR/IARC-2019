import subprocess


# TODO - Readd print statements to rtg

# TODO - RTG cannot pan?

class IPC:
    # Should be used in python 2.7
    # Different commands for windows and linux ?
    # Python 3 must be able to be run from python3 command
    # Must have packages installed that tools will use

    os_windows = True

    pyfile = "../real_time_graphing"

    def __init__(self):
        import sys

        # TODO - Make use of stdout and stdin
        self.splitter = subprocess.Popen('python3 data_splitter.py', stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        # TODO - Do not use stdout=PIPE or stderr=PIPE with this function as that can deadlock based on the child process output volume. Use Popen with the communicate() method when you need pipes.

        sleep(.5)  # Poll will return None if immediately called after creating obj
        if self.splitter.poll():
            output, error_output = self.splitter.communicate()

            print(error_output)
            self.splitter = subprocess.Popen('python3 tools/ipc/data_splitter.py', stdin=subprocess.PIPE,
                                             stderr=subprocess.PIPE, stdout=subprocess.PIPE)

            output, error_output = self.splitter.communicate()
            if error_output: print(error_output)

    def send(self, data):
        if self.splitter.poll() is None:
            self.splitter.stdin.write("{}\n".format(str(data).encode()))  # Not optimal

            print("IPC: {}".format(str(data)))
            # print(self.splitter.stdout.readline())  # Blocks until line sent
            #self.splitter.communicate(input=str(data))  # Communicate hangs for some reason

        else:
            print("IPC: Cannot send data")


if __name__ == '__main__':
    from math import sin, cos
    from time import sleep

    demo = IPC()

    sleep(1)
    for j in range(10000):
        # Only able to send data once
        i = j * 3.14
        demo.send({
            'altitude': sin(i),
            'airspeed': cos(i),
            'velocity_x': sin(i),
            'velocity_y': cos(i),
            'velocity_z': sin(i),
            'voltage': cos(i),
            'roll': cos(i),
            'pitch': sin(i),
            'yaw': cos(i),
            'target_altitude': sin(i),
            'target_pitch_velocity': cos(i),
            'target_roll_velocity': cos(i),
            'target_yaw': sin(i)
        })

        sleep(.1)

        if demo.splitter.poll() is not None:
            print("IPC: splitter.poll(): {}".format(demo.splitter.poll()))
            break

    print("IPC: Done sending data.")
    demo.splitter.terminate()
