
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
        
        date = time.strftime('%x') #Gets todays date
        newDate = date.replace('/','_') #changes the / for _ to not mess us the directory
        dailyFlight = 1

        while(i<1):
            self.directory = 'C:/Users/jonat/Desktop/MultiRotor_Logging/{}_Flight_Num_{}.csv'.format(newDate,str(dailyFlight))
            if not os.path.exists(self.directory): #checks to see if the path already exists
                open(self.directory,'a').close #if it doesn't exist it makes it
                i = 5
            else:
                dailyFlight = dailyFlight + 1
        self.start = time.time()
        with open(self.directory,"w") as f:
            self.dataValues = ['secFromStart','airSpeed','altitude','pitch','roll','yaw','xVelocity','yVelocity','zVelocity','voltage'] #defining the headers
            writer = csv.DictWriter(f, fieldnames=self.dataValues) #definng the headers
            writer.writeheader()
        self.g = open(self.directory,"a")
    
    def exit(self):
        self.g.close()

    def Update(self,inputData):    
             
                currentTime = time.time()
            
                writer = csv.DictWriter(self.g, fieldnames=self.dataValues)
                writer.writerow({
                'secFromStart' : (currentTime - self.start),
                'airSpeed' : inputData['airspeed'],
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


my_logger = Logger()


myData = {}
while (x<theTempCounter):
    #make data dictionary here
    myData = {
        'airspeed' : random.randint(0,10),
        'altitude' : random.randint(0,10),
        'pitch' : random.randint(0,10),
        'roll' : random.randint(0,10),
        'yaw' : random.randint(0,10),
        'velocity_x' : random.randint(0,10),
        'velocity_y' : random.randint(0,10),
        'velocity_z' : random.randint(0,10),
        'voltage' : random.randint(0,10),
    }
    my_logger.Update(myData)
    x = x + 1
my_logger.exit()