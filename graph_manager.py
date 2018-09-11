# The graph manager, takes input, interprets and passes on relevant data to individual graphs

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

from weakref import ref

from value_generator import get_next_value


class GraphManager(object):
    def __init__(self, pan=-1, save=False, graph=False):
        
        # Stores what will be graphed (ex. 'pitch', 'roll', 'yaw')
        self.graph = [] 
        
        # Stores the pan window measured in seconds
        self.pan = pan
        
        # Stores True is saving, False if not
        self.save = save
        
        # Turn on interactive mode
        plt.ion()

        # Get figure for Pyplot
        self.figure = plt.figure()
       
        numrows = len(graph)
        current = 1
        
        # Stores the axes for each thing to be graphed
        self.axes_dictionary = {}

        # Stores the data frame (df) for each thing to be graphed
        self.df_dictionary = {}

        # Configuring the figure
        for g in graph:
            name = g[0]
            target = g[1]

            self.graph.append(name)

            self.axes_dictionary[name] = self.figure.add_subplot(numrows, 1, current)
            
            self.axes_dictionary[name].set_title("{}{}".format(name[0:1].upper(), name[1:]))
            self.axes_dictionary[name].set_ylabel('PID Value')
           
            # Sets the target line, which will be present for 1800 seconds (10 minutes)
            self.axes_dictionary[g[0]].plot([0, 1800], [target, target], label='Target')
            
            if self.pan > 0:
                self.axes_dictionary[name].set_xlim(left=0, right=self.pan)

            else:
                self.axes_dictionary[name].set_xlim(left=0.0, right=0.01)

            self.df_dictionary[name] = pd.DataFrame({"Seconds":[], "PID":[]})
            current += 1
            
        self.figure.subplots_adjust(hspace=1)
        self.startTime = time.time()
        
        if save:
            self.checkPoint = self.startTime

    def dispatch_update(self, ax, df, new_x, tag):
        # 0th line is the target line
        # 1st line is the old line
        if len(ax.lines) > 1:
            ax.lines[1].remove()

        df = df.append({"Seconds":new_x, "PID":get_next_value(new_x)}
                , ignore_index=True)
        df.plot(x="Seconds", y="PID", ax=ax, 
                legend=None, color='blue')

        if self.pan > 0:
            if new_x > self.pan:
                ax.set_xlim(left=new_x - self.pan, right=new_x)
        else:
            ax.set_xlim(right=new_x)
  
        return df
        
    def update(self):
        now = time.time()
        diff = now - self.startTime

        for key in self.graph:            
            self.df_dictionary[key] = self.dispatch_update(
                    self.axes_dictionary[key], 
                    self.df_dictionary[key], 
                    diff, 
                    key[0:1])

        if self.save:
            # save every 5 seconds
            if now - self.checkPoint > 5:
                self.checkPoint = now
                plt.savefig(self.save)

    def run(self, speed=0.05):
        if speed <= 0:
            speed = 0.05
        while True:
            self.update()
            plt.pause(speed)
