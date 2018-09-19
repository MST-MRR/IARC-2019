# A sample controller to demonstrate the abilities of the grapher

import sys  # sys.exit()

from graph_manager import GraphManager

from matplotlib.pyplot import pause
from numpy import random  # random.rand()

import traceback  # traceback.format_exc()
import logging  # logging.error()


def main():
    # Create Graph Manager Object
    test_graph = GraphManager()

    # Number of values to send per update
    values_to_pass = 8

    # Demo Simulation Loop
    i = 0

    while True:
        i += 1

        try:
            test_graph.update({  # key and value not key and list!!!!!!!!!
                'Target_Update_Demo': i,
                'Pitch': [[i * 10 + v for v in range(values_to_pass)], random.rand(values_to_pass)],
                'Yaw': [[i * 10 + v for v in range(values_to_pass)], random.rand(values_to_pass)],
                'Roll': [[i * 10 + v for v in range(values_to_pass)], random.rand(values_to_pass)]
            })

            pause(.05)

        except Exception as e:
            print("Quitting: {}".format(e))
            logging.error((traceback.format_exc()))
            break

    sys.exit()


if __name__ == '__main__':
    main()
