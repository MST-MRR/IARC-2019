import import_parent_directory

from time import sleep

from demo_data_gen import get_demo_data

from interprocess_communication import IPC


if __name__ == '__main__':
    print("IPC: Should graph randomly for a few seconds.")

    with IPC() as demo:
        for i in range(0, 500, 3):
            demo.send(get_demo_data())

            sleep(.1)

            if not demo.alive:
                break
