import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

startTime = time.time()

def getNextValue(d):
    ret = np.cos([d])[0]
    return ret
    
df = pd.DataFrame({"Seconds":[], "y":[]})

plt.ion()
fig, ax = plt.subplots()
while True:
    diff = time.time() - startTime
    df = df.append({"Seconds":diff, "y":getNextValue(diff)}, ignore_index=True)
    ax.clear()
    df.plot(x="Seconds", y="y", ax=ax)
    plt.draw()
    plt.pause(0.05)
plt.show()

