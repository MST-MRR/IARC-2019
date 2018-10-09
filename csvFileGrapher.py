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
    data_file = filedialog.askopenfilename(
        title="Select file to Graph", filetypes=(("csv files", "*.csv"), ("all files", "*.*"))
    )

    # pick the file for the settings
    config_file = filedialog.askopenfilename(
        title="Select the Graphing Config file", filetypes=(("csv files", "*.csv"), ("all files", "*.*"))
    )

    root.destroy()  # Close the tkinter window

    #
    # Read data & config
    df = pd.read_csv(data_file)  # Read data

    with open(config_file, 'r') as file:
        data_to_plot, relevant_intervals  = list(csv.reader(file))  # Read config file

    #
    # Get ready to plot data
    minLimit = float(relevant_intervals[0])  # gets the min and max limts for graphing
    maxLimit = float(relevant_intervals[1])

    #
    # Plot data
    for dataToPlot in data_to_plot:  # plots each data point based on the other settings
        maxTime = df['secFromStart'] < maxLimit
        minTime = df['secFromStart'] > minLimit

        new = df[maxTime & minTime]

        x = new['secFromStart']
        y = new[dataToPlot]

        plt.plot(x, y)

    plt.legend()  # Enable legend

    plt.show()  # Show the matplotlib plot


if __name__ == '__main__':
    make_whole_graph()
