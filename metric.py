# For the graphs metric line

import pandas as pd


# Maybe use built in pandas/numpy data structure instead
class Metric:
    def __init__(self, x_axis_label, y_axis_label, name, color, func):
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label

        # Init
        self.__name = name  # Name of metric

        self.__legend = "{}{}".format(name[0:1].upper(), name[1:])

        self.__color = color

        self.__func = func  # Function to generate values

        # Change to map?
        # Create cache
        self.__cache = pd.DataFrame({self.x_axis_label: [], self.y_axis_label: []})  # Stores generated values

    def get_name(self):
        return self.__name

    def get_legend(self):
        return self.__legend

    def get_color(self):
        return self.__color

    def get_func(self):
        return self.__func

    def get_cache(self):
        return self.__cache

    def set_legend(self):
        self.__legend = "_nolegend_"

    def set_func(self, func):
        self.__func = func

    def set_cache(self, data):
        self.__cache = self.__cache.append(data, ignore_index=True)

    def generate_values(self, input_values):
        # Turn x, y, target values into generator to access differently

        generated_values = [self.__func(value) for value in input_values[self.y_axis_label]]

        # Add generated data to cache
        self.set_cache(
            pd.DataFrame({self.x_axis_label: input_values[self.x_axis_label], self.y_axis_label: generated_values}))