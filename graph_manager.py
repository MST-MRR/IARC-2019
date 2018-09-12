# The graph manager, handles all graphs wanted by config file

import matplotlib.pyplot as plt
import pandas as pd

from graph import Graph

xlabel = "My X Label"
ylabel = "My Y Label"

class GraphManager(object):
    def __init__(self):
        # Read config file

        plt.ion()

        self.graph_settings = self.read_config()

        self.desired_graphs = ['Pitch', 'Roll']

        self.figure = plt.figure()

        # Load from graph_settings
        self.graphs = {'Pitch': Graph('Pitch', self.figure, xlabel, ylabel, 1, 1, len(self.desired_graphs)), 'Roll': Graph('Roll', self.figure, xlabel, ylabel, 2, 1, len(self.desired_graphs))}

        self.temporary_ieterator = 1

    def read_config(self):
        return []

    def update(self):
        # Pull dictionary from json

        # new_data = self.read_json()

        # new_data will be dictionary

        # Pull relevant values based on config and send them

        new_data = {'Pitch': [[1, 2, 3, 4, 5, 6, 7, 8],[1, 2, 3, 4, 5, 6, 7, 8]], 'Yaw': [[2, 1, 4, 3, 6, 5, 8, 7],[2, 1, 4, 3, 6, 5, 8, 7]], 'Roll': [[2, 1, 4, 3, 6, 5, 8, 7],[2, 1, 4, 3, 6, 5, 8, 7]]}

        for key, value in new_data.items():
            if key in self.desired_graphs:
                self.graphs[key].update(pd.DataFrame({xlabel:[x + (10 * self.temporary_ieterator) for x in value[0]], ylabel:value[1]}))
        
        self.temporary_ieterator += 1