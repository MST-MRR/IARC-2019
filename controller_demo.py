# A sample controller to demonstrate the abilities of the grapher

import sys  # sys.exit()

from graph_manager import GraphManager

import matplotlib.pyplot as plt  # plt.pause()


def main():
    # Create Graph Manager Object
    test_graph = GraphManager()

    i = 0

    # Demo Simulation Loop
    while True:
        i += 1

        try:
            test_graph.update(i)

            plt.pause(.05)

        except Exception as e:
            print("Quitting: {}".format(e))
            break

    sys.exit()


if __name__ == '__main__':
    main()
