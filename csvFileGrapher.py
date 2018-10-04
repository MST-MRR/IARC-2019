import csv

from tkinter import filedialog
from tkinter import Tk

import pandas as pd
import matplotlib.pyplot as plt


def make_whole_graph():
    """
    Use:
    """

    #
    # Get startup data

    root = Tk()  # Create tkinter window

    # Select data to graph through explorer prompt
    fileToUse = filedialog.askopenfilename(
        initialdir="", title="Select file to Graph", filetypes=(("csv files", "*.csv"), ("all files", "*.*"))
    )

    # pick the file for the settings
    configFile = filedialog.askopenfilename(
        initialdir="", title="Select the Graphing Config file", filetypes=(("csv files", "*.csv"), ("all files", "*.*"))
    )

    root.destroy()  # Close the tkinter window

    #
    # Read csv
    df = pd.read_csv(fileToUse)
    df.head()

    with open(configFile, 'r') as s:  # makes the config file into a list of lists
        reader = csv.reader(s)
        configMainList = list(reader)

    #
    # Get ready to plot data
    configList = configMainList[0]  # pulls the first list of which headers to graph together
    intervalList = configMainList[1]  # pulls the second list of what time interval to graph

    minLimit = float(intervalList[0])  # gets the min and max limts for graphing
    maxLimit = float(intervalList[1])

    #
    # Plot data
    for dataToPlot in configList:  # plots each data point based on the other settings
        maxTime = df['secFromStart'] < maxLimit
        minTime = df['secFromStart'] > minLimit
        new = df[maxTime & minTime]
        x = new['secFromStart']
        y = new[dataToPlot]

        plt.plot(x, y)

    plt.legend()  # Display legend for plot

    plt.show()  # Show the matplotlib plot


if __name__ == '__main__':
    make_whole_graph()
