import os, sys, inspect

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

sys.path.insert(0, parent_dir)


from time import sleep

from demo_data_gen import get_demo_data

from interprocess_communication import IPC


if __name__ == '__main__':
    print("IPC: Should graph randomly for 10 seconds.")

    with IPC() as demo:
        for i in range(0, 100, 3):
            demo.send(get_demo_data())

            sleep(.1)

            if not demo.alive:
                break
