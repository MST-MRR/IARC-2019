# A sample controller to demonstrate the abilities of the grapher

import sys  # sys.exit()
from argparse import ArgumentParser

import matplotlib.pyplot as plt

from graph_manager import GraphManager

from value_generator import get_next_value


def main():
    # Parse command line arguments, - for demo
    parser = ArgumentParser(description='Takes in flags --pan <seconds wide>, --save <filename>, <graphs_to_display>')

    parser.add_argument('-p', '--pan', type=int, nargs='?', default='100')

    parser.add_argument('-s', '--save', type=str, nargs='?', default='graph.png')

    parser.add_argument('to_graph', type=str, nargs='*')

    args = parser.parse_args()

    # Initialize necessary components
    test_graph = GraphManager()  # Remove need to add target immediately

    speed = .05

    i = 0  # for generating values

    # Simulation loop
    while True:
        i += 1

        
        # # Only update when new data comes in
        test_graph.update()  # get_next_value(i)
        plt.pause(speed)

        # grapher.render()



    sys.exit()


if __name__ == '__main__':
    main()
