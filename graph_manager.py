# The graph manager -> handles all graphs. Options in config file

import matplotlib.pyplot as plt
import pandas as pd

from timer import timeit

from graph import Graph


class GraphManager(object):
    """
    Use: GraphManager()

        Creates & manages individual graphs. What to plot / keep track of is set in the graph config file. Data comes
        in from GraphManager.update()

    Variables:  # TODO
        self.graph_settings:  Settings read in from the config file.  (self.read_config())

        self.figure: Figure that the subplots (Graph objects) go on.  (plt.figure())

        self.graphs: Dictionary that holds all graph objects and their unique ids

    Functions:
        update(): Sends any new data to relevant graph objects

        read_config(): Reads config file & returns interpreted version

        interpret_data(): Parses data from drone

        add_graph(title): Starts tracking new data, title is used as unique id and subplot title

        add_tracker(graph, title, func): Adds new tracker(line) to specified graph w/ specified metric
    """

    graphs_per_column = 3  # Formatting variable, how many graphs per column before loop

    def __init__(self):

        # Get Startup Data
        self.graph_settings = self.read_config()

        #
        # Setup Matplot
        plt.ion()  # Enable interactive graphs
        self.figure = plt.figure()  # Figure that the subplots (Graph objects) go on

        self.figure.subplots_adjust(hspace=1)  # Create a buffer space between subplots to avoid overlap

        #
        # Initialize Graph Data Storage
        self.graphs = {}  # Dictionary that holds the graph objects and their unique ids

        # Add desired graphs where they belong
        [self.add_graph(wanted_graph) for wanted_graph in self.graph_settings['Desired Graphs'].keys()]

    # TODO
    def read_config(self):
        """
        Use: To read and interpret the graph config file

        Returns: Dictionary parsed from config file
        """

        return {'Desired Graphs': {'Pitch': ['Pitch_x', 'Pitch_y'], 'Roll': ['Roll_x', 'Roll_y']}}

    def add_graph(self, title):
        """
        Use: To begin tracking new data

        Parameters:
            title: Unique id & subplot title
        """

        self.graphs[title] = Graph(
            self.figure, title,
            self.graph_settings['Desired Graphs'][title][0],
            self.graph_settings['Desired Graphs'][title][1],
            len(self.graphs) % GraphManager.graphs_per_column + 1,
            len(self.graphs) / GraphManager.graphs_per_column + 1,
            len(self.graph_settings['Desired Graphs'].keys())
        )

        # REMOVE when better controller - Functionality demo
        self.graphs[title].update_target(.4)

        self.graphs[title].add_metric('testeroni', lambda x: x / 3)

    # TODO - Implement
    def add_tracker(self, graph, title, func):
        """
        Use: To add new tracker to specified graph

        Parameters:
            graph: What graph to add tracker too
            title: Title of tracker
            func: Metric function to graph based on
        """

        assert graph in self.graphs.keys(), "Graph '{}' not available.".format(graph)

        self.graphs[graph].add_metric(title, func)

    def interpret_data(self, messy_data):
        """
        Use: Interpret data as it comes in from drone

        Parameters:
            messy_data: Data to be cleaned

        Returns:
            clean_data: Only the values in data that are also in graphs.keys()
                    # TODO -> may need separate desired_values from graphs.keys()
        """

        clean_data = {}

        [clean_data.update({key: value}) if key in self.graphs.keys() else None for key, value in messy_data.items()]

        return clean_data

    @timeit
    def update(self, incoming_data, **kwargs):
        """
        Use: To add new data to graphs

        Parameters:
            incoming_data: Dictionary w/ all info sent from drone, gets parsed w/ interpret_data()
        """

        new_data = self.interpret_data(incoming_data)

        for key, value in new_data.items():
            self.graphs[key].update(pd.DataFrame({self.graphs[key].x_axis_label: value[0], self.graphs[key].y_axis_label: value[1]}))

        # TODO REMOVE when better controller - Functionality demo
        target_updates = incoming_data['Target_Update_Demo']  # Will be changed when data parsing is done
        self.graphs['Roll'].update_target(int(target_updates / 100))
