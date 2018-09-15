# A sample controller to demonstrate the abilities of the grapher

import sys  # sys.exit()

from graph_manager import GraphManager

import matplotlib.pyplot as plt  # plt.pause()

import numpy as np  # random.rand

import time

def main():
    # Create Graph Manager Object
    test_graph = GraphManager()

    i = 0

    # Demo Simulation Loop
    def loop(i):
        try:
            test_graph.update({
                'Target_Update_Demo': i,
                'Pitch': [[i * 10 + v for v in range(8)], np.random.rand(8)],
                'Yaw': [[i * 10 + v for v in range(8)], np.random.rand(8)],
                'Roll': [[i * 10 + v for v in range(8)], np.random.rand(8)]
            })

            plt.pause(.05)

        except Exception as e:
            print("Quitting: {}".format(e))
            return False

        return i+1

    while i + 1:
        i = loop(i)

    sys.exit()


if __name__ == '__main__':
    main()
