# The graph manager -> handles all graphs. Options in config file

import matplotlib.pyplot as plt
import pandas as pd

import xml.etree.ElementTree as ET  # https://www.geeksforgeeks.org/xml-parsing-python/

from timer import timeit

from graph import Graph


class GraphManager(object):
    """
    Use: GraphManager()

        Creates & manages individual graphs. What to plot / keep track of is set in the graph config file. Data comes
        in from GraphManager.update()

    Variables:
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

    config_filename = 'config.xml'

    graphs_per_column = 3  # Formatting variable, how many graphs per column before loop

    def __init__(self):

        # Get Startup Data
        self.__graph_settings = self.read_config()

        #
        # Setup Matplot
        plt.ion()  # Enable interactive graphs
        self.__figure = plt.figure()  # Figure that the subplots (Graph objects) go on

        self.get_figure().subplots_adjust(hspace=1)  # Create a buffer space between subplots to avoid overlap

        #
        # Initialize Graph Data Storage
        self.__graphs = {}  # Dictionary that holds the graph objects and their unique ids

        # Add desired graphs where they belong
        [self.add_graph(wanted_graph) for wanted_graph in self.get_graph_settings()['Desired Graphs'].keys()]

    def read_config(self):
        """
        Use: To read and interpret the graph config file

        Returns: Dictionary parsed from config file
        """

        # XML file structure
        """
        root
            Data:
                x: 1
                y: 2

     Currently only desired graphs
            Desired Graphs
                Graph: Title, x_label, y_label
                    Metrics
                        Metric: Title, function
                        Metric: Title, function
                        
                Graph: Title, x_label, y_label
                    Metrics
                        Metric: Title, funciton
        """

        # Get root
        root = ET.parse(GraphManager.config_filename).getroot()

        xml_dict = {}

        xml_dict.update({'Desired Graphs': {}})

        for graph in root.findall('graph'):
            xml_dict['Desired Graphs'].update(
                {graph.get('title'): [graph.get('xlabel'),
                                      graph.get('ylabel'),
                                      [[metric.get('title'),
                                        metric.get('func'),
                                        metric.get('color')
                                        ] for metric in graph.findall('metric')]]}
            )

        return xml_dict

    def get_graph_settings(self):
        """
        Returns: self.__graph_settings
        """
        return self.__graph_settings

    def get_figure(self):
        """
        Returns: self.__figure
        """
        return self.__figure

    def get_graphs(self):
        """
        Returns: self.__graphs
        """
        return self.__graphs

    def add_graph(self, title):
        """
        Use: To begin tracking new data

        Parameters:
            title: Unique id & subplot title
        """

        self.__graphs[title] = Graph(
            self.get_figure(), title,
            self.get_graph_settings()['Desired Graphs'][title][0],
            self.get_graph_settings()['Desired Graphs'][title][1],
            len(self.get_graphs()) % GraphManager.graphs_per_column + 1,
            len(self.get_graphs()) / GraphManager.graphs_per_column + 1,
            len(self.get_graph_settings()['Desired Graphs'])
        )

        # Adds graph metrics read in from xml
        for metric, func, color in self.get_graph_settings()['Desired Graphs'][title][2]:
            self.add_tracker(title, metric, func, color)

        # TODO REMOVE when better controller - Functionality demo
        self.get_graphs()[title].update_target(.4)

    def add_tracker(self, graph, title, func, color=None):
        """
        Use: To add new tracker to specified graph

        Parameters:
            graph: What graph to add tracker too
            title: Title of tracker
            func: Metric function to graph based on
            color: Line color
        """

        assert graph in self.get_graphs().keys(), "Graph '{}' not available.".format(graph)

        self.get_graphs()[graph].add_metric(title, func, color)

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

        [clean_data.update({key: value}) if key in self.get_graphs().keys() else None for key, value in messy_data.items()]

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
            self.get_graphs()[key].update(pd.DataFrame(
                {self.get_graphs()[key].get_x_axis_label(): value[0], self.get_graphs()[key].get_y_axis_label(): value[1]}))

        # TODO REMOVE when better controller - Functionality demo
        target_updates = incoming_data['Target_Update_Demo']  # Will be changed when data parsing is done
        self.get_graphs()['Roll'].update_target(int(target_updates / 100) / 2)
