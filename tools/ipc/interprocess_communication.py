from __future__ import print_function

import os
import subprocess


class IPC:
    # Should be used in python 2.7
    # Different commands for windows and linux ?

    os_windows = True

    pyfile = "../real_time_graphing"

    def __init__(self):
        self.splitter = os.popen('python3 data_splitter.py')

        # TODO - Create rtg
        self.rtg = None

        # TODO - Create data splitter
        # self.splitter = None

    def send(self, data):
        # TODO - Send data to splitter object
        pass


if __name__ == '__main__':
    from math import sin, cos
    from time import sleep

    demo = IPC()

    for i in range(100):
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

        print(demo.splitter.poll())
