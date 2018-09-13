#This is for Logging the Voltage
import time
import SettingsLogging
import csv
from random import randint

def init():
    f = open(SettingsLogging.voltage,'w') #opens a file (first variable) in write mode (w) and stores in f
    

    with f:
        writer = csv.writer(f) #this opens the mode into writing mode (?)
        velValues = ['timeStamp', 'secFromStart', 'dataValue'] #defining the headers
        writer = csv.DictWriter(f, fieldnames=velValues) #definng the headers
        writer.writeheader()

def run():
    localtime = time.strftime('%a %I %M %S') #gets the local time in (Day Hour Minute Second) form and stores in localtime
    current = time.time()
    numTime = current - SettingsLogging.start
    value = randint(0, 10) #temporary for testing with random input values
    with open(SettingsLogging.voltage,'a') as g: #opens the same file as before but now in append mode (a)
        velValues = ['timeStamp', 'secFromStart', 'dataValue']
        writer = csv.DictWriter(g, fieldnames=velValues)
        writer.writerow({'timeStamp' : localtime, 'secFromStart' : numTime, 'dataValue' : value})
        #This is white the variable in the section titled at the left of the ':'