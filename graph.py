# The individual graphs w/ all relevant data tracking

import pandas as pd


class Graph(object):
    """
    Use:

    Functions:

    """

    config = {'main': 'blue', 'target': 'orange'}

    def __init__(self, title, figure, x_label, y_label, row, col, total_num, target=None, pan=None):
        self.title = title

        self.axis = figure.add_subplot(total_num, col, row)
        self.axis.set_title(self.title)

        self.x_label = x_label
        self.y_label = y_label

        self.axis.set_ylabel(self.y_label)

        self.data = pd.DataFrame({self.x_label: [], self.y_label: []})

        self.target = target
        self.pan = pan
        
    def update(self, new_data):
        """
        Use: To add new data to graph

        Parameters:
            new_data: Data to be added to graph
        """

        self.data = self.data.append(new_data, ignore_index=True)

        for line in self.axis.lines:
            if line.get_color() == 'blue':
                self.axis.lines.remove(line)
            #if line.get_color() == 'orange':
             #   self.axis.lines.remove(line)

        # Only plot relevant data
        self.data.iloc[-300:].plot(x=self.x_label, y=self.y_label, ax=self.axis, legend=None, color=self.config['main'])

        if self.pan:
            right = self.data.tail(1)[self.x_label].iloc[0]
            self.axis.set_xlim(left=right - self.pan, right=right+100)

    def plot_target(self):
        # Target could be dots plotted from last update to this update? then purged

        # Set target line
        if self.target:
            self.axis.axhline(y=self.target, xmin=0, xmax=100, color=self.config['target'])

    def set_target(self, new_target):
        """
        Use: To update target value

        Parameters:
            new_target: New target value
        """

        self.target = new_target

        self.plot_target()

    def add_analysis(self, f):
        """
        Use: To add new tracker to graph

        Parameters:
            f:
        """

        pass

