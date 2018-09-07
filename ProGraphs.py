import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time


def getNextValue(d):
    ret = np.cos([d])[0]
    return ret


class Grapher(object):
    def __init__(self):
        self.startTime = time.time()
    
        self.df = pd.DataFrame({"Seconds":[], "y":[]})

        plt.ion()

        self.fig, self.ax = plt.subplots()

    def update(self):
        diff = time.time() - self.startTime
        self.df = self.df.append({"Seconds":diff, "y":getNextValue(diff)}, ignore_index=True)
        self.ax.clear()
        self.df.plot(x="Seconds", y="y", ax=self.ax)
        plt.draw()


if __name__ == '__main__':
    graph_test = Grapher()

    while True:
        graph_test.update()
        plt.pause(0.05)

    #plt.show()
