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

        for line in self.axis.lines:
            if line.get_color() == 'blue':
                self.axis.lines.remove(line)


        # Only plot the new data (set color to something to avoid rainbow effect)
        ax =  self.data.iloc[-300 : ]\
            .plot(x=self.x_label, y=self.y_label, ax=self.axis, legend=None, color='blue') 

        # Old code that plots every data point upon call to this function
        #self.data.plot(x=self.x_label, y=self.y_label, ax=self.axis, legend=None, color='blue')

        if self.pan:
            right = self.data.tail(1)[self.x_label].iloc[0]
            self.axis.set_xlim(left=right - self.pan, right=right)

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

