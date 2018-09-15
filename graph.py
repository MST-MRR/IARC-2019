# The individual graphs w/ all relevant data tracking

import warnings  # To suppress UserWarning associated w/ using _nolegend_

import pandas as pd


class Graph(object):
    """
    Use:
        To keep track of certain data points. Each line's unique id is its color

    Functions:

    """

    # Maybe use built in pandas/numpy data structure instead
    class Metric:
        def __init__(self, x_label, y_label, name, func):
            self.x_label = x_label
            self.y_label = y_label

            # Init
            self.__name = name  # Name of metric

            self.__func = func  # Function to generate values

            # Change to map?
            # Create cache
            self.__cache = pd.DataFrame({self.x_label: [], self.y_label: []})  # Stores generated values

        def get_name(self):
            return self.__name

        def get_func(self):
            return self.__func

        def get_cache(self):
            return self.__cache

        def set_cache(self, data):
            self.__cache = self.__cache.append(data, ignore_index=True)

        def generate_values(self, input_values):
            generated_values = [self.__func(value) for value in input_values[self.y_label]]

            # Add generated data to cache
            self.set_cache(pd.DataFrame({self.x_label: input_values[self.x_label], self.y_label: generated_values}))

    def __init__(self, figure, title, x_label, y_label, row, col, total_num, target=None, pan=300):
        # Configuration settings
        self.config = {'main': ['blue', 'Main'], 'target': ['orange', 'Target']}
        self.get_available_color = iter(['red', 'yellow', 'green', 'cyan', 'black'])

        # Create & add subplot to figure
        self.axis = figure.add_subplot(total_num, col, row)

        # Title of the graph & this objects unique identifier
        self.title = title
        self.axis.set_title(self.title)

        # X and Y axis labels
        self.x_label = x_label
        self.y_label = y_label

        # Set axis labels
        #self.axis.set_xlabel(self.x_label)
        self.axis.set_ylabel(self.y_label)

        # Main data points
        self.data = pd.DataFrame({self.x_label: [], self.y_label: []})

        # Optional variables
        self.target = target  # TODO - Turn into metric
        self.pan = pan

        # Desired metrics
        self.metrics = [self.Metric(self.x_label, self.y_label, 'main', lambda x: x)]

    # TODO?
    def update(self, new_data):
        """
        Use: To add new data to graph

        Parameters:
            new_data: Data to be added to graph
        """

        # Add new data to data
        self.data = self.data.append(new_data, ignore_index=True)

        # # How to update individual line?

        # Only plot relevant data
        #relevant_data = self.data.iloc[-300:]
        #self.plot_line('main', relevant_data)

        for metric in self.metrics:
            metric.generate_values(new_data)

        for metric in self.metrics:
            if not metric.get_cache().empty:
                # TODO - Update panning to pan based on x axis
                self.plot_line(metric.get_name(), metric.get_cache()[-self.pan:])

        # Handle display panning
        if self.pan:
            right = self.data.tail(1)[self.x_label].iloc[0]
            self.axis.set_xlim(left=right - self.pan, right=right+100)

    # TODO?
    def plot_line(self, unique_id, data, color=None):
        # NOT TESTED
        # Add a configuration if not already one
        if unique_id not in self.config.keys():
            self.config[unique_id] = [color if color else next(self.get_available_color), unique_id[0:1].upper() + unique_id[1:]]

        #
        # Purge old line before setting new one
        for line in self.axis.lines:
            if line.get_color() == self.config[unique_id][0]:
                self.axis.lines.remove(line)

        #
        # Plot line
        with warnings.catch_warnings():
            # Suppress label="_nolegend_" warning
            warnings.simplefilter("ignore")

            # Plot line
            data.plot(x=self.x_label, y=self.y_label, ax=self.axis, label=self.config[unique_id][1], color=self.config[unique_id][0])

        # Patch for redundant legend entries
        if self.config[unique_id][1] is not "_nolegend_": self.config[unique_id][1] = "_nolegend_"

    # TODO
    def plot_target(self):
        # # Phase out # #

        # # # Target could be dots plotted from last update to this update? then purged

        if self.target: self.axis.axhline(y=self.target, xmin=0, xmax=100, color=self.config['target'][0])

    # TODO
    def update_target(self, new_target):
        """
        Use: To update target value

        Parameters:
            new_target: New target value
        """

        self.target = new_target

        # # # Cannot purge in future

        # Purge old target line ?
        for line in self.axis.lines:
            if line.get_color() == self.config['target'][0]:
                self.axis.lines.remove(line)

        # TODO
        # print(self.data[self.y_label].iloc[-1] if len(self.data[self.y_label]) > 0 else 0)

        self.plot_line("target", pd.DataFrame(
            {
                self.x_label: [
                    # FIX
                    self.data[self.y_label].iloc[-1] if len(self.data[self.y_label]) > 0 else 0,
                    20000],
                self.y_label: [self.target, self.target]
            }
        ))

    def add_metric(self, title, func):
        """
        Use: To add new metric to graph

        Parameters:
            title: Name of metric
            func: Function for metric to execute
        """
        print(title)
        print(func(2))

        self.metrics.append(self.Metric(self.x_label, self.y_label, title, func))


