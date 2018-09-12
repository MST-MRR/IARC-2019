# A sample controller to demonstrate the abilities of the grapher

import sys  # sys.exit()

from graph_manager import GraphManager

import matplotlib.pyplot as plt  # plt.pause()


def main():
    # Create graph manager
    test_graph = GraphManager()

    # Simulation loop
    while True:

        # # Only update when new data comes in
        test_graph.update()
        plt.pause(.05)

    sys.exit()


if __name__ == '__main__':
    main()
