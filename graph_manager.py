# The graph manager, handles all graphs wanted by config file

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from graph import Graph


class GraphManager(object):
    """
    Use:
        GraphManager()

        Creates & manages 1+ individual graphs. What to plot / keep track of is set in the graph config file

    Functions:
        update(): Sends any new data to relevant graphs

        read_config(): Reads config file & returns interpreted version

        add_graph(title): Starts tracking new data, title is used as unique id and subplot title
    """

    graphs_per_column = 3  # Formatting variable, how many graphs per column before loop

    def __init__(self):

        # Get Startup Data
        self.graph_settings = self.read_config()

        #
        # Setup Matplot
        plt.ion()  # Enable interactive graphs
        self.figure = plt.figure()  # Figure that the subplots (Graph objects) go on

        # Create a buffer space between subplots to avoid overlap
        self.figure.subplots_adjust(hspace=1)

        #
        # Initialize Graph Data Storage
        self.desired_graphs = []  # The desired graphs (May be redundant depending on how data comes in)

        self.graphs = {}  # Dictionary that holds the graph objects and their unique ids

        # Add desired graphs to where they belong
        [self.add_graph(wanted_graph) for wanted_graph in self.graph_settings.keys()]

        # For our current value generation system, to be removed in future
        self.temporary_iterator = 1

    def read_config(self):
        """
        Use: To read and interpret the graph config file

        Returns: Dictionary parsed from config file
        """

        return {'Pitch': ['Pitch_x', 'Pitch_y'], 'Roll': ['Roll_x', 'Roll_y']}

    def add_graph(self, title):
        """
        Use: To begin tracking new data

        Parameters:
            title: Unique id & subplot title
        """

        self.desired_graphs.append(title)

        self.graphs[title] = Graph(
            self.figure, title, self.graph_settings[title][0], self.graph_settings[title][1],
            len(self.graphs) % GraphManager.graphs_per_column + 1,
            len(self.graphs) / GraphManager.graphs_per_column + 1,
            len(self.graph_settings.keys())
        )

        self.graphs[title].update_target(.4)

    def update(self, data):
        """
        Use: To add new data to graphs

        Parameters:
            data: Dictionary w/ all info sent from drone, needs to be parsed
        """

        # Pull dictionary from json

        # new_data = self.read_json()

        # new_data will be dictionary

        # Pull relevant values based on config and send them

        target_updates = data  # Will be changed when data parsing is done
        self.graphs['Roll'].update_target(int(target_updates / 100))

        new_data = {
            'Pitch': [[1, 2, 3, 4, 5, 6, 7, 8], np.random.rand(8)],
            'Yaw':   [[1, 2, 3, 4, 5, 6, 7, 8], np.random.rand(8)],
            'Roll':  [[1, 2, 3, 4, 5, 6, 7, 8], np.random.rand(8)]
        }

        for key, value in new_data.items():
            if key in self.desired_graphs:
                self.graphs[key].update(
                    pd.DataFrame({
                        self.graphs[key].x_label: [x + (10 * self.temporary_iterator) for x in value[0]],
                        self.graphs[key].y_label: value[1]
                    })
                )
        
        self.temporary_iterator += 1
