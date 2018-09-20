
import csv
import os
from tkinter import filedialog
from tkinter import Tk
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


#gets the file you want graphed through an explorer prompt
root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
fileToUse = root.filename

df = pd.read_csv(fileToUse)
df.head()

runTillStop = 'y'
while(runTillStop == 'y'):
    dataToPlot = input("What data value to plot? (use proper header!) ")
    x = df['secFromStart']
    y = df[dataToPlot]
    
    plt.plot(x,y)
    runTillStop = input("Graph another data set?(y/n) ")

plt.show()
