import pandas as pd


class Graph(object):

    def __init__(self, title, figure, xlabel, ylabel, row, col, total_num, target=None, pan=None):
        self.title = title
        self.axis = figure.add_subplot(total_num, col, row)
        self.axis.set_title(title)
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.data = pd.DataFrame({self.xlabel:[], self.ylabel:[]})
        self.target = target
        self.pan = pan
        
    def update(self, new_data):
        self.data = self.data.append(new_data, ignore_index=True)
        self.data.plot(x=self.xlabel, y=self.ylabel, ax=self.axis, 
                legend=None, color='blue')
        # TODO: Add target point functionality

    def setTarget(self, new_target):
        self.target = new_target

    def addAnalysis(self, f):
        pass

