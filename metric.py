# A trackable metric that can be plotted on a graph

import pandas as pd


class Metric:
    def __init__(self, x_axis_label, y_axis_label, name, color, func):

        self.__x_axis_label = x_axis_label
        self.__y_axis_label = y_axis_label

        self.__name = name  # Name of metric

        self.__legend = "{}{}".format(name[0:1].upper(), name[1:])  # Legend entry key

        self.__color = color  # Line color

        self.__func = func  # Value generation function

        self.__cache = pd.DataFrame({self.get_x_axis_label(): [], self.get_y_axis_label(): []})  # Stores generated values

    def get_x_axis_label(self):
        """

        """

        return self.__x_axis_label

    def get_y_axis_label(self):
        """

        """

        return self.__y_axis_label

    def get_name(self):
        """

        """

        return self.__name

    def get_legend(self):
        """

        """

        return self.__legend

    def get_color(self):
        """

        """

        return self.__color

    def get_func(self):
        """

        """

        return self.__func

    def get_cache(self):
        """

        """

        return self.__cache

    def set_legend(self):
        """

        """

        if not self.__legend == "_nolegend_": self.__legend = "_nolegend_"

    def set_func(self, func):
        """

        """

        self.__func = func

    def set_cache(self, data):
        """

        """

        self.__cache = self.__cache.append(data, ignore_index=True)

    def generate_values(self, target, input_values):
        """

        """

        if not target:
            target = 0

        generated_values = [self.__func(value, target) for value in input_values[self.get_y_axis_label()]]

        # Add generated data to cache
        self.set_cache(
            pd.DataFrame({self.get_x_axis_label(): input_values[self.get_x_axis_label()], self.get_y_axis_label(): generated_values}))
