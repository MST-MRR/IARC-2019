from tkinter import filedialog
from tkinter import Tk

import pandas as pd
import matplotlib.pyplot as plt

from tools.file_io.file_io import parse_config


def make_whole_graph():
    """
    Builds graph from logging files.

    Needs:
    """

    #
    # Get startup data
    root = Tk()  # Create tkinter window

    # Select config & data to graph through explorer prompt
    config_file = filedialog.askopenfilename(
        title="Select the Graphing Config file",
        filetypes=(("xml files", "*.xml"), ("csv files", "*.csv"), ("all files", "*.*"))
    )

    file_type_wanted = "*{}*.csv".format(config_file.replace(".xml", "").split("/")[-1])

    data_file = filedialog.askopenfilename(
        title="Select file to Graph", filetypes=((file_type_wanted, file_type_wanted), ("csv files", "*.csv"), ("all files", "*.*"))
    )

    root.destroy()  # Close the tkinter window

    #
    # Read data & config
    raw_data = pd.read_csv(data_file)

    config = parse_config(config_file)

    fig = plt.figure()

    for i, graph in enumerate(config):
        columns_to_plot = [metric['x_stream'] for metric in graph['metric']]

        #
        # Prepare data
        min_time_limit = float(graph['lower_time']) if graph['lower_time'] else 0
        max_time_limit = float(graph['upper_time']) if graph['upper_time'] else 100000

        rows_below_max = raw_data['secFromStart'] < max_time_limit
        rows_above_min = raw_data['secFromStart'] > min_time_limit

        parsed_data = raw_data[rows_below_max & rows_above_min]

        graphs_per_col = 3

        ax = fig.add_subplot(min(graphs_per_col, len(config)), len(config) // graphs_per_col + 1, i + 1)

        #
        # Plot data
        for column in columns_to_plot:
            ax.plot(parsed_data['secFromStart'], parsed_data[column])  # x, y

        plt.legend()  # Enable legend

    plt.show()  # Show the matplotlib plot


if __name__ == '__main__':
    make_whole_graph()
