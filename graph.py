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
            self.set_cache(pd.DataFrame({self.x_axis_label: input_values[self.x_axis_label], self.y_axis_label: generated_values}))

    def __init__(self, figure, title, x_axis_label, y_label, row, col, total_num, target=None, pan=300):
        # Configuration settings
        #self.config = {'main': ['blue', 'Main'], 'target': ['orange', 'Target']}
        self.get_available_color = iter(['red', 'yellow', 'green', 'cyan', 'black'])

        # Create & add subplot to figure
        self.axis = figure.add_subplot(total_num, col, row)

        # Title of the graph & this objects unique identifier
        self.title = title
        self.axis.set_title(self.title)

        # X and Y axis labels
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_label

        # Set axis labels
        #self.axis.set_xlabel(self.x_axis_label)
        self.axis.set_ylabel(self.y_axis_label)

        # Main data points
        self.data = pd.DataFrame({self.x_axis_label: [], self.y_axis_label: []})

        # Optional variables
        self.target = target  # TODO - Turn into metric
        self.pan = pan

        # Desired metrics
        self.metrics = {
            'main': self.Metric(self.x_axis_label, self.y_axis_label, 'main', 'blue', lambda x: x),
            "target": self.Metric(self.x_axis_label, self.y_axis_label, "target", "orange", lambda x: self.target)
        }

    def update(self, new_data):
        """
        Use: To add new data to graph

        Parameters:
            new_data: Data to be added to graph
        """

        # Add new data to data
        self.data = self.data.append(new_data, ignore_index=True)

        for metric in self.metrics.values():
            metric.generate_values(new_data)

        for metric in self.metrics.values():
            if not metric.get_cache().empty:
                # TODO - Update panning to pan based on x axis
                self.plot_line(metric.get_name(), metric.get_cache()[-self.pan:])

        # Handle display panning
        if self.pan:
            right = self.data.tail(1)[self.x_axis_label].iloc[0]
            self.axis.set_xlim(left=right - self.pan, right=right+100)

    # TODO?
    def plot_line(self, unique_id, data, color=None):
        # Add a configuration for metric if not already one
        #if unique_id not in self.config.keys():
        #    self.config[unique_id] = [color if color else next(self.get_available_color), unique_id[0:1].upper() + unique_id[1:]]

        #
        # Purge old line before setting new one
        for line in self.axis.lines:
            if line.get_color() == self.metrics[unique_id].get_color():
                self.axis.lines.remove(line)

        #
        # Plot line
        with warnings.catch_warnings():
            # Suppress label="_nolegend_" warning
            warnings.simplefilter("ignore")

            # Plot line
            data.plot(x=self.x_axis_label, y=self.y_axis_label, ax=self.axis, label=self.metrics[unique_id].get_legend(), color=self.metrics[unique_id].get_color())

        # Patch for redundant legend entries
        self.metrics[unique_id].set_legend()

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

        self.metrics['target'].set_func(lambda x: self.target)

        # # # Cannot purge in future

        # Purge old target line ?
        #for line in self.axis.lines:
         #   if line.get_color() == self.config['target'][0]:
          #      self.axis.lines.remove(line)

        # TODO
        # print(self.data[self.y_axis_label].iloc[-1] if len(self.data[self.y_axis_label]) > 0 else 0)

        #self.plot_line("target", pd.DataFrame(
         #   {
          #      self.x_axis_label: [
           #         # FIX
            #        self.data[self.y_axis_label].iloc[-1] if len(self.data[self.y_axis_label]) > 0 else 0,
             #       20000],
              #  self.y_axis_label: [self.target, self.target]
            #}
        #))

    def add_metric(self, title, func):
        """
        Use: To add new metric to graph

        Parameters:
            title: Name of metric
            func: Function for metric to execute
        """

        self.metrics.update({title: self.Metric(self.x_axis_label, self.y_axis_label, title, next(self.get_available_color), func)})


