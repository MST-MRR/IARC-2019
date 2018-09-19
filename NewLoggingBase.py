
import time
import csv
import os
from math import trunc
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

    def Update(self):    

            with open(self.directory,'a') as g:
                currentTime = time.time()
                timeFromStart = '%0.3f' % (currentTime - self.start)
                airSpeed = 1#airSpeedInput
                altitude = 2#altitudeInput
                pitch = 3#pitchInput
                roll = 4#rollInput
                yaw = 5#yawInput
                xVelocity = 6#xVelocityInput
                yVelocity = 7#yVelocityInput
                zVelocity = 8#zVelocityInput
                voltage = 9#voltageInput

                writer = csv.DictWriter(g, fieldnames=self.dataValues)
                writer.writerow({'secFromStart':timeFromStart,'airSpeed':airSpeed,'altitude':altitude,'pitch':pitch,'roll':roll,'yaw':yaw,'xVelocity':xVelocity,'yVelocity':yVelocity,'zVelocity':zVelocity,'voltage':voltage})
                #This is white the variable in the section titled at the left of the ':'


my_logger = Logger()


while (x<theTempCounter):
    my_logger.Update()
    x = x + 1