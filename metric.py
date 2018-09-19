# A trackable metric that can be plotted on a graph

import pandas as pd


class Metric:
    def __init__(self, x_axis_label, y_axis_label, name, color, func):

        self._x_axis_label = x_axis_label
        self._y_axis_label = y_axis_label

        self._name = name  # Name of metric

        self._legend = "{}{}".format(name[0:1].upper(), name[1:])  # Legend entry key

        self._color = color  # Line color

        self._func = func  # Value generation function

        # change to buffer
        self._buffer = pd.DataFrame({self.get_x_axis_label(): [], self.get_y_axis_label(): []})  # Stores generated values

    def get_x_axis_label(self):
        """

        """

        return self._x_axis_label

    def get_y_axis_label(self):
        """

        """

        return self._y_axis_label

    def get_name(self):
        """

        """

        return self._name

    def get_legend(self):
        """

        """

        return self._legend

    def get_color(self):
        """

        """

        return self._color

    def get_func(self):
        """

        """

        return self._func

    def get_cache(self):
        """

        """

        return self._buffer

    def set_legend(self):
        """

        """

        if not self._legend == "_nolegend_": self._legend = "_nolegend_"

    def set_func(self, func):
        """

        """

        self._func = func

    def set_cache(self, data):
        """

        """

        self._buffer = self._buffer.append(data, ignore_index=True)

    def generate_values(self, target, input_values):
        """

        """

        if not target:
            target = 0

        generated_values = [self._func(value, target) for value in input_values[self.get_y_axis_label()]]

        # Add generated data to cache
        self.set_cache(
            pd.DataFrame({self.get_x_axis_label(): input_values[self.get_x_axis_label()], self.get_y_axis_label(): generated_values}))
