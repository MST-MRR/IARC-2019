# The graph manager, handles all graphs wanted by config file

import matplotlib.pyplot as plt

from graph import Graph


class GraphManager(object):
    def __init__(self):
        # Read config file

        self.graph_settings = self.read_config()

        self.desired_graphs = ['Pitch', 'Roll']

        self.figure = plt.figure()

        # Load from graph_settings
        self.graphs = {'Pitch': Graph('Pitch', self.figure, 1, 1), 'Roll': Graph('Roll', self.figure, 2, 1)}

    def read_config(self):
        return []

    def update(self):
        # Pull dictionary from json

        # new_data = self.read_json()

        # new_data will be dictionary

        # Pull relevant values based on config and send them

        new_data = {'Pitch': [1, 2, 3, 4, 5, 6, 7, 8], 'Yaw': [2, 1, 4, 3, 6, 5, 8, 7], 'Roll': [2, 1, 4, 3, 6, 5, 8, 7][::-1]}

        for key, value in new_data.items():
            if key in self.desired_graphs:
                self.graphs[key].update(value)
