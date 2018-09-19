
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

    def Update(self,inputData):    
             
            with open(self.directory,'a') as g:
                currentTime = time.time()
                timeFromStart = '%0.3f' % (currentTime - self.start)
                airSpeed = inputData['airspeed']#airSpeedInput
                altitude = inputData['altitude']#altitudeInput
                pitch = inputData['pitch']#pitchInput
                roll = inputData['roll']#rollInput
                yaw = inputData['yaw']#yawInput
                xVelocity = inputData['velocity_x']#xVelocityInput
                yVelocity = inputData['velocity_y']#yVelocityInput
                zVelocity = inputData['velocity_z']#zVelocityInput
                voltage = inputData['voltage']#voltageInput

                writer = csv.DictWriter(g, fieldnames=self.dataValues)
                writer.writerow({'secFromStart':timeFromStart,'airSpeed':airSpeed,'altitude':altitude,'pitch':pitch,'roll':roll,'yaw':yaw,'xVelocity':xVelocity,'yVelocity':yVelocity,'zVelocity':zVelocity,'voltage':voltage})
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