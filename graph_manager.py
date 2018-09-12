# The graph manager, handles all graphs wanted by config file

import matplotlib.pyplot as plt
import pandas as pd

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

        #
        # # Get Startup Data

        # Read configuration file to see what should be graphed
        self.graph_settings = self.read_config()

        #
        # # Setup Matplot

        # Set up matplot figure
        plt.ion()  # Enable interactive graphs
        self.figure = plt.figure()  # Figure that the subplots (Graph objects) go on

        #
        # # Initialize Graph Data Storage

        # The desired graphs (May be redundant depending on how data comes in)
        self.desired_graphs = []

        # Dictionary that holds the graph objects and their unique ids
        self.graphs = {}

        # Add desired graphs to where they belong
        for wanted_graph in self.graph_settings.keys():
            self.add_graph(wanted_graph)

        #
        # # Misc

        # For out current value generation system, to be removed in future
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
            title, self.figure, self.graph_settings[title][0], self.graph_settings[title][1],
            len(self.graphs) % GraphManager.graphs_per_column + 1,
            len(self.graphs) / GraphManager.graphs_per_column + 1,
            len(self.graph_settings.keys())
        )

    def update(self):
        """
        Use: To add new data to graphs
        """

        # Pull dictionary from json

        # new_data = self.read_json()

        # new_data will be dictionary

        # Pull relevant values based on config and send them

        new_data = {
            'Pitch': [[1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8]],
            'Yaw':   [[1, 2, 3, 4, 5, 6, 7, 8], [2, 1, 4, 3, 6, 5, 8, 7]],
            'Roll':  [[1, 2, 3, 4, 5, 6, 7, 8], [2, 1, 4, 3, 6, 5, 8, 7]]
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
