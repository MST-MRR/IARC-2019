# A sample controller to demonstrate the abilities of the grapher

import sys  # sys.exit()

from graph_manager import GraphManager

import matplotlib.pyplot as plt  # plt.pause()

import numpy as np  # random.rand
import traceback
import logging

def main():
    # Create Graph Manager Object
    test_graph = GraphManager()

    # Demo Simulation Loop
    i = 0
    time_log = {}
    while True:
        i += 1

        values_to_pass = 8

        try:
            test_graph.update({
                'Target_Update_Demo': i,
                'Pitch': [[i * 10 + v for v in range(values_to_pass)], np.random.rand(values_to_pass)],
                'Yaw': [[i * 10 + v for v in range(values_to_pass)], np.random.rand(values_to_pass)],
                'Roll': [[i * 10 + v for v in range(values_to_pass)], np.random.rand(values_to_pass)]
            }, log_time=time_log)

            print(time_log)

            plt.pause(.05)

        except Exception as e:
            print("Quitting: {}".format(e))
            logging.error((traceback.format_exc()))
            break

    sys.exit()


if __name__ == '__main__':
    main()
