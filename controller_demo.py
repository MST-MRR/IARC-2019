# A sample controller to demonstrate the abilities of the grapher

import sys  # sys.exit()

from graph_manager import GraphManager

import matplotlib.pyplot as plt  # plt.pause()

import numpy as np  # random.rand


def main():
    # Create Graph Manager Object
    test_graph = GraphManager()

    i = 0

    # Demo Simulation Loop
    while True:
        i += 1

        try:
            test_graph.update({
                'Target_Update_Demo': i,
                'Pitch': [[1, 2, 3, 4, 5, 6, 7, 8], np.random.rand(8)],
                'Yaw': [[1, 2, 3, 4, 5, 6, 7, 8], np.random.rand(8)],
                'Roll': [[1, 2, 3, 4, 5, 6, 7, 8], np.random.rand(8)]
            })

            plt.pause(.05)

        except Exception as e:
            print("Quitting: {}".format(e))
            break

    sys.exit()


if __name__ == '__main__':
    main()
