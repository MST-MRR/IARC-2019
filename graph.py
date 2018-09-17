# The individual graphs w/ all relevant data tracking

import warnings  # To suppress UserWarning associated w/ using _nolegend_

import pandas as pd

from metric import Metric


class Graph(object):
    """
    Use:
        To keep track of certain data points. Each line's unique id is its color

    Functions:

    """

    def __init__(self, figure, title, x_axis_label, y_axis_label, row, col, total_num, target=None, pan=300):
        # Color generator for metrics
        self.get_available_color = iter(['red', 'yellow', 'green', 'cyan', 'black', None])

        # Create & add subplot to figure
        self.__axis = figure.add_subplot(total_num, col, row)

        # Title of the graph & this objects unique identifier
        self.__title = title
        self.get_axis().set_title(self.get_title())

        # X and Y axis labels
        self.__x_axis_label = x_axis_label
        self.__y_axis_label = y_axis_label

        # Set axis labels
        #self.axis.set_xlabel(self.get_x_axis_label())
        self.get_axis().set_ylabel(self.get_y_axis_label())

        # Main data points
        #self.data = pd.DataFrame({self.get_x_axis_label(): [], self.get_y_axis_label(): []})

        # Misc variables
        self.__target = target
        self.__pan = pan

        # Tracked metrics
        self.metrics = {}

    def get_axis(self):
        """
        Returns: self.__axis
        """

        return self.__axis

    def get_title(self):
        """
        Returns: self.__title
        """

        return self.__title

    def get_x_axis_label(self):
        """
        Returns: self.__x_axis_label
        """

        return self.__x_axis_label

    def get_y_axis_label(self):
        """
        Returns: self.__y_axis_label
        """

        return self.__y_axis_label

    def get_target(self):
        """
        Returns: self.__target
        """

        return self.__target

    def get_pan(self):
        """
        Returns: self.__pan
        """

        return self.__pan

    def update(self, new_data):
        """
        Use: To add new data to graph

        Parameters:
            new_data: Data to be added to graph
        """

        # Add new data to data
        #self.data = self.data.append(new_data, ignore_index=True)

        #
        # Generate new metric values
        for metric in self.metrics.values():
            metric.generate_values(self.get_target(), new_data)

        #
        # Render each metric
        for metric in self.metrics.values():
            if not metric.get_cache().empty:
                self.plot_line(metric.get_name(), metric.get_cache()[-self.get_pan():])

        #
        # Handle display panning
        if self.get_pan():
            #right = self.data.tail()[self.get_x_axis_label()].iloc[0]

            right = new_data[self.get_x_axis_label()].iloc[-1]

            self.get_axis().set_xlim(left=right - self.get_pan(), right=right+100)

    def plot_line(self, unique_id, data):
        """
        Use: Plot selected metric w/ specified data

        Parameters:
            unique_id: Metric to plot
            data: Data to plot
        """

        assert unique_id in self.metrics.keys(), "'{}' is not currently being tracked!"

        # Purge old line before setting new one
        for line in self.get_axis().lines:
            if line.get_color() == self.metrics[unique_id].get_color():
                self.get_axis().lines.remove(line)

        #
        # Plot line
        # TODO - possible slowdown
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  # Suppress label="_nolegend_" warning
            data.plot(x=self.get_x_axis_label(), y=self.get_y_axis_label(), ax=self.get_axis(),
                      label=self.metrics[unique_id].get_legend(), color=self.metrics[unique_id].get_color())

        # Patch for redundant legend entries
        self.metrics[unique_id].set_legend()

    def update_target(self, new_target):
        """
        Use: To update target value

        Parameters:
            new_target: New target value
        """

        self.__target = new_target

    def add_metric(self, title, func, color=None):
        """
        Use: To add new metric to graph

        Parameters:
            title: Name of metric
            func: Function for metric to execute
            color: Specify line color. Default: get_available_color
        """

        self.metrics.update({title: Metric(self.get_x_axis_label(), self.get_y_axis_label(), title,
                                           color if color else next(self.get_available_color),
                                           lambda x, t: eval(func) if type(func) is str else func)})

        assert self.metrics[title].get_color, "Ran out of colors to give lines!"
