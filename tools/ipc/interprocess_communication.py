import subprocess
from time import sleep

# TODO - RTG cannot pan?

# TODO - Way to pass in custom splitter filename?

# TODO - Make sure everything works from multiple start locations

# TODO - ERROR, WARNING, INFO


class IPC:
    # Should be used in python 2.7
    # Python 3 must be able to be run from python3 command

    def __init__(self):
        for filename in ['data_splitter.py', 'tools/ipc/data_splitter.py']:
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

    def send(self, data):
        if self.splitter.poll() is None:
            try:
                self.splitter.stdin.write("{}\n".format(str(data).encode()))  # Lots of warnings against stdin!
            except IOError as e:
                print(e)

            print("IPC: {}".format(str(data)))
        else:
            print("IPC: Cannot send data")


def shell_reader(splitter, thread_stop):
    # TODO - Build reader and its thread into the IPC class!

    while not thread_stop.is_set():
        out = splitter.stdout.readline().strip()  # output w/out \n
        if not out == "": print(out)


if __name__ == '__main__':
    import threading

    from math import sin, cos

    thread_stop = threading.Event()

    demo = IPC()

    threads = {'output_reader': threading.Thread(target=shell_reader, args=(demo.splitter, thread_stop,))}

    for thread in threads.values():
        thread.start()

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

        if demo.splitter.poll() is not None or thread_stop.is_set():
            print("IPC: splitter.poll(): {}".format(demo.splitter.poll()))
            break

    print("IPC: Done sending data.")
    demo.splitter.terminate()

    thread_stop.set()

    for thread in threads.values():
        thread.join()
