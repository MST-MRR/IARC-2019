import csv

from tkinter import filedialog
from tkinter import Tk

import pandas as pd
import matplotlib.pyplot as plt


def make_whole_graph():
    """
    Builds graph from logging files.
    """

    #
    # Get startup data
    root = Tk()  # Create tkinter window

    # Select data to graph through explorer prompt
    # TODO - From config??

    data_file = filedialog.askopenfilename(
        title="Select file to Graph", filetypes=(("csv files", "*.csv"), ("all files", "*.*"))
    )

    # pick the file for the settings
    # TODO - By default?

    config_file = filedialog.askopenfilename(
        title="Select the Graphing Config file", filetypes=(("csv files", "*.csv"), ("all files", "*.*"))
    )

    root.destroy()  # Close the tkinter window


    # TODO - make read data file generally

    #
    # Read data & config
    df = pd.read_csv(data_file)  # Read data

    with open(config_file, 'r') as file:
        data_to_plot, relevant_intervals = list(csv.reader(file))  # Read config file

    # TODO - improve below - concise

    #
    # Get ready to plot data
    min_time_limit = float(relevant_intervals[0])  # gets the min and max limts for graphing
    max_time_limit = float(relevant_intervals[1])

    rows_below_max = df['secFromStart'] < max_time_limit
    rows_above_min = df['secFromStart'] > min_time_limit

    data = df[rows_below_max & rows_above_min]

    #
    # Plot data
    for column in data_to_plot:  # plots each data point based on the other settings
        x = data['secFromStart']
        y = data[column]

        plt.plot(x, y)

    plt.legend()  # Enable legend

    plt.show()  # Show the matplotlib plot


if __name__ == '__main__':
    make_whole_graph()
