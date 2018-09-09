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
        for g in graph:
            if g[0] == 'pitch':
                # Configuring the graph (factor into a new function?)
                self.graph.append('pitch')
                self.ax_p = self.figure.add_subplot(numrows, 1, current)
                self.ax_p.set_title('Pitch')
                self.ax_p.set_ylabel('PID Value')
                self.ax_p.plot([0, 1800], [g[1], g[1]], label='Target')
                if self.pan > 0:
                    self.ax_p.set_xlim(left=0, right=self.pan)
                else:
                    self.ax_p.set_xlim(left=0.0, right=0.01)
                self.df_p = pd.DataFrame({"Seconds":[], "PID":[]})
                current += 1
            if g[0] == 'yaw':
                self.graph.append('yaw')
                self.ax_y = self.figure.add_subplot(numrows, 1, current)
                self.ax_y.set_title('Yaw')
                self.ax_y.set_ylabel('PID Value')
                self.ax_y.plot([0, 1800], [g[1], g[1]], label='Target')
                if self.pan > 0:
                    self.ax_y.set_xlim(left=0, right=self.pan)
                else:
                    self.ax_y.set_xlim(left=0.0, right=0.01) 
                self.df_y = pd.DataFrame({"Seconds":[], "PID":[]})
                current += 1
            if g[0] == 'roll':
                self.graph.append('roll')
                self.ax_r = self.figure.add_subplot(numrows, 1, current)
                self.ax_r.set_title('Roll')
                self.ax_r.set_ylabel('PID Value')
                self.ax_r.plot([0, 1800], [g[1], g[1]], label='Target')
                if self.pan > 0:
                    self.ax_r.set_xlim(left=0, right=self.pan)
                else:
                    self.ax_r.set_xlim(left=0.0, right=0.01) 
                self.df_r = pd.DataFrame({"Seconds":[], "PID":[]})
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

        df = df.append({"Seconds":new_x, "PID":getNextValue(new_x)}
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
        for element in self.graph:
            if element == 'pitch':
                self.df_p = self.dispatch_update(self.ax_p, 
                        self.df_p, diff, 'p')
            if element == 'yaw':
                self.df_y = self.dispatch_update(self.ax_y, 
                        self.df_y, diff, 'y')
            if element == 'roll':
                self.df_r = self.dispatch_update(self.ax_r, 
                        self.df_r, diff, 'r')

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
