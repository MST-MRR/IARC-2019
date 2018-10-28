import csv

from tkinter import filedialog
from tkinter import Tk

import pandas as pd
import matplotlib.pyplot as plt

from tools.file_io.file_io import parse_config


def make_whole_graph():
    """
    Builds graph from logging files.
    """

    #
    # Get startup data
    root = Tk()  # Create tkinter window

    # Select data to graph through explorer prompt
    # TODO - From config??

    # Way to start of zoomed

    #
    #
    # TODO - Make read in associated files based on config -> if only one config file read it

    # pick the file for the settings
    # TODO - By default?

    config_file = filedialog.askopenfilename(
        title="Select the Graphing Config file",
        filetypes=(("xml files", "*.xml"), ("csv files", "*.csv"), ("all files", "*.*"))
    )

    data_file = filedialog.askopenfilename(
        title="Select file to Graph", filetypes=(("csv files", "*.csv"), ("all files", "*.*"))
    )

    root.destroy()  # Close the tkinter window


    # TODO - make read data file generally

    #
    # Read data & config
    df = pd.read_csv(data_file)  # Read data

    config = parse_config(config_file)[0]

    data_to_plot = [metric['x_stream'] for metric in config['metric']]

    #
    # Prepare data
    min_time_limit = float(config['lower_time']) if config['lower_time'] else 0
    max_time_limit = float(config['upper_time']) if config['upper_time'] else 100000

    rows_below_max = df['secFromStart'] < max_time_limit
    rows_above_min = df['secFromStart'] > min_time_limit

    data = df[rows_below_max & rows_above_min]

    #
    # Plot data
    for column in data_to_plot:  # plots each data point based on the other settings
        plt.plot(data['secFromStart'], data[column])  # x, y

    plt.legend()  # Enable legend

    plt.show()  # Show the matplotlib plot


if __name__ == '__main__':
    make_whole_graph()
