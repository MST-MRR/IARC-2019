
import csv
import os
from tkinter import filedialog
from tkinter import Tk
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


#gets the file you want graphed through an explorer prompt
root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file to Graph",filetypes = (("csv files","*.csv"),("all files","*.*")))
fileToUse = root.filename

root.settings = filedialog.askopenfilename(initialdir = "/",title = "Select the Graphing Config file",filetypes = (("csv files","*.csv"),("all files","*.*")))
configFile = root.settings

df = pd.read_csv(fileToUse)
df.head()

with open(configFile, 'r') as s:
    reader = csv.reader(s)
    configMainList = list(reader)

configList = configMainList[0]
intervalList = configMainList[1]
i = 0
j = len(configList)
minLimit = float(intervalList[0])
maxLimit = float(intervalList[1])

while (i < j):
    dataToPlot = configList[i]
    maxTime = df['secFromStart'] < maxLimit    
    minTime = df['secFromStart'] > minLimit
    new = df[maxTime & minTime] 
    x = new['secFromStart']
    y = new[dataToPlot]

    plt.plot(x,y)
    i = i + 1


plt.show()
