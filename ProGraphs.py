import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

from weakref import ref

from ProValueGenerator import getNextValue

class Grapher(object):
    def __init__(self, pan=-1, save=False, graph=False):

        self.graph = [] 
         
        self.pan = pan
        
        self.save = save
        
        plt.ion()

        self.figure = plt.figure()
        
        numrows = len(graph)
        current = 1
        if 'pitch' in graph:
            self.graph.append('pitch')
            self.ax_p = self.figure.add_subplot(numrows, 1, current)
            self.ax_p.set_title('Pitch')
            self.df_p = pd.DataFrame({"x":[], "y":[]})
            current += 1
        if 'yaw' in graph:
            self.graph.append('yaw')
            self.ax_y = self.figure.add_subplot(numrows, 1, current)
            self.ax_y.set_title('Yaw')
            self.df_y = pd.DataFrame({"x":[], "y":[]})
            current += 1
        if 'roll' in graph:
            self.graph.append('roll')
            self.ax_r = self.figure.add_subplot(numrows, 1, current)
            self.ax_r.set_title('Roll')
            self.df_r = pd.DataFrame({"x":[], "y":[]})
            current += 1
 
        self.startTime = time.time()
        
        if save:
            self.checkPoint = self.startTime

    def dispatch_update(self, ax, df, new_x, tag):
        # 0th line is the target line
        # 1st line is the old line
        if len(ax.lines) > 1:
            ax.lines[1].remove()

        df = df.append({"x":new_x, "y":getNextValue(new_x)}
                , ignore_index=True)
        ax.set_xlim(auto=True)
        df.plot(x="x", y="y", ax=ax, 
                legend=None, color='blue')

        if self.pan > 0:
            left, right = ax.get_xlim()
            if right > self.pan:
                ax.set_xlim(left=right - self.pan)
  
        return df
        

    def update(self):
        now = time.time()
        diff = now - self.startTime
        for element in self.graph:
            if element == 'pitch':
                self.df_p = self.dispatch_update(self.ax_p, 
                        self.df_p, diff, 'p')
            if element == 'yaw':
                self.df_y = self.dispatch_update(self.ax_y, 
                        self.df_y, diff, 'y')
                self.ax_y.set_title('Yaw')
            if element == 'roll':
                self.df_r = self.dispatch_update(self.ax_r, 
                        self.df_r, diff, 'r')
                self.ax_r.set_title('Roll')

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
