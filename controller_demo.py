# A sample controller to demonstrate the abilities of the grapher

import sys  # sys.exit()

import matplotlib.pyplot as plt

from graph_manager import GraphManager

from value_generator import get_next_value


def main():
    test_graph = GraphManager(graph=[('roll', 1)])

    speed = .05

    i = 0  # for generating values

    while True:
        i += 1
        try:
            test_graph.update()  # get_next_value(i)
            plt.pause(speed)

            # grapher.render()

        except:
            print("Hit exception")
            # break

    sys.exit()

if __name__ == '__main__':
    main()
