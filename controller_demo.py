# A sample controller to demonstrate the abilities of the grapher

import sys  # sys.exit()

from graph_manager import GraphManager

import matplotlib.pyplot as plt  # plt.pause()

import numpy as np  # random.rand

import time


def main():
    # Create Graph Manager Object
    test_graph = GraphManager()

    # Demo Simulation Loop
    def loop(i):
        values_to_pass = 8

        time_log = {}

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
            return False

        return i+1

    i = 0
    while i is not False:
        i = loop(i)

    sys.exit()


if __name__ == '__main__':
    main()
