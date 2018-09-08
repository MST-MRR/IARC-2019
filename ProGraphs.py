import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

from ProValueGenerator import getNextValue


class Grapher(object):
    def __init__(self, pan=-1, save=False):
        self.pan = pan
        
        self.save = save

        self.startTime = time.time()
        
        if save:
            self.checkPoint = self.startTime
    
        self.df = pd.DataFrame({"Seconds":[], "y":[]})

        plt.ion()

        self.fig, self.ax = plt.subplots()
        
    def update(self):
        now = time.time()
        diff = now - self.startTime
        self.df = self.df.append({"Seconds":diff, "y":getNextValue(diff)}, ignore_index=True)
        self.ax.clear()
        self.df.plot(x="Seconds", y="y", ax=self.ax)
        if self.pan > 0:
            left, right = self.ax.get_xlim()
            if right > self.pan:
                self.ax.set_xlim(right - self.pan, right)
 
        if self.save:
            # save every 5 seconds
            if now - self.checkPoint > 5:
                self.checkPoint = now
                plt.savefig(self.save)


        plt.draw()

    def run(self, speed=0.05):
        if speed <= 0:
            speed = 0.05
        while True:
            self.update()
            plt.pause(speed)
