
import time
import csv
import os
import random

#tempCounter is how many data point to collect temporarily

theTempCounter = int(input("How many data points? "))
x = 0

class Logger:

    def __init__(self):
        i = 0
        self.lastTime = 0
        date = time.strftime('%x') #Gets todays date
        newDate = date.replace('/','_') #changes the / for _ to not mess us the directory
        dailyFlight = 1

        while(i<1):
            self.directory = 'C:/Users/jonat/Desktop/MultiRotor_Logging/{}_Flight_Num_{}.csv'.format(newDate,str(dailyFlight))
            if not os.path.exists(self.directory): #checks to see if the path already exists
                open(self.directory,'a').close #if it doesn't exist it makes it
                i = 5
            else:# keep adding the daily flight num till a new one is found
                dailyFlight = dailyFlight + 1
        self.start = time.time()#gets initial time
        with open(self.directory,"w") as f:#opens the file to write the headers
            self.dataValues = ['secFromStart','airSpeed','altitude','pitch','roll','yaw','xVelocity','yVelocity','zVelocity','voltage'] #defining the headers
            writer = csv.DictWriter(f, fieldnames=self.dataValues) #definng the headers
            writer.writeheader()
        self.g = open(self.directory,"a")#Open the file in appending to add the new data
    
    def exit(self):#defines the funtion to close the file
        self.g.close()

    def Update(self,inputData):#updates the file with the new data
             
                currentTime = time.time()

                if (self.lastTime != currentTime):
                    writer = csv.DictWriter(self.g, fieldnames=self.dataValues)
                    writer.writerow({
                    'secFromStart' : (currentTime - self.start),#the time stamp for the data
                    'airSpeed' : inputData['airspeed'], #the headers to store
                    'altitude' : inputData['altitude'],
                    'pitch' : inputData['pitch'],
                    'roll' : inputData['roll'],
                    'yaw' : inputData['yaw'],
                    'xVelocity' : inputData['velocity_x'],
                    'yVelocity' : inputData['velocity_y'],
                    'zVelocity' : inputData['velocity_z'],
                    'voltage' : inputData['voltage']
                    })
                    #This is white the variable in the section titled at the left of the ':'

                self.lastTime = currentTime


my_logger = Logger()


myData = {}
while (x<theTempCounter):#main loop
    #make data dictionary here
    myData = {
        'airspeed' : 1*x,
        'altitude' : 2*x,
        'pitch' : 3*x,
        'roll' : 4*x,
        'yaw' : 5*x,
        'velocity_x' : 6*x,
        'velocity_y' : 7*x,
        'velocity_z' : 8*x,
        'voltage' : 9*x,
    }
    my_logger.Update(myData)
    x = x + 1
my_logger.exit()