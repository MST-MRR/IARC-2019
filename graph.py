import pandas as pd


class Graph(object):
    """
    Use:

    Functions:

    """

    def __init__(self, title, figure, x_label, y_label, row, col, total_num, target=None, pan=None):
        self.title = title

        self.axis = figure.add_subplot(total_num, col, row)
        self.axis.set_title(self.title)

        self.x_label = x_label
        self.y_label = y_label

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

        # Number of new data items
        new_items = len(new_data[self.x_label])

        # Number of data items in the data frame
        total = self.data.shape[0]

        # Only plot the new data (set color to something to avoid rainbow effect)
        self.data.iloc[total - new_items - 1 : total]\
            .plot(x=self.x_label, y=self.y_label, ax=self.axis, legend=None) 

        # Old code that plots every data point upon call to this function
        #self.data.plot(x=self.x_label, y=self.y_label, ax=self.axis, legend=None, color='blue')

        # TODO: Add target point functionality

    def set_target(self, new_target):
        """
        Use: To update target value

        Parameters:
            new_target: New target value
        """

        self.target = new_target

    def add_analysis(self, f):
        """
        Use: To add new tracker to graph

        Parameters:
            f:
        """

        pass

