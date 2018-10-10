import time
import csv
import os
import random


class Logger:
    """
    Object that can be sent data to be logged
    """
    def __init__(self, desired_data=None):
        self.desired_data = ['airspeed', 'altitude', 'pitch', 'roll', 'yaw', 'velocity_x', 'velocity_y',
                             'velocity_z', 'voltage'] if not desired_data else desired_data

        self.dataValues = ['secFromStart'] + self.desired_data
        # ['secFromStart', 'airSpeed', 'altitude', 'pitch', 'roll', 'yaw', 'xVelocity', 'yVelocity', 'zVelocity', 'voltage']  # defining the headers

        i = 0
        self.lastTime = 0
        date = time.strftime('%x') #Gets todays date
        newDate = date.replace('/','_') #changes the / for _ to not mess us the directory
        dailyFlight = 1

        while(i<1):
            self.directory = '{}_Flight_Num_{}.csv'.format(newDate,str(dailyFlight))
            if not os.path.exists(self.directory): #checks to see if the path already exists
                open(self.directory,'a').close #if it doesn't exist it makes it
                i = 5
            else:# keep adding the daily flight num till a new one is found
                dailyFlight = dailyFlight + 1
        self.start = time.time()#gets initial time
        with open(self.directory,"w") as f:#opens the file to write the headers

            writer = csv.DictWriter(f, fieldnames=self.dataValues) #definng the headers
            writer.writeheader()
        self.g = open(self.directory,"a")#Open the file in appending to add the new data
    
    def exit(self):#defines the funtion to close the file
        """
        Closes file that was logging data.
        """

        self.g.close()

    def Update(self, inputData):  # updates the file with the new data
        """
        Send new data to be logged.

        Parameters
        ----------
        inputData: dict
            Stream of new data to be logged
        """
        currentTime = time.time()

        stopWhile = currentTime - self.start

        if self.lastTime != currentTime:
            writer = csv.DictWriter(self.g, fieldnames=self.dataValues)

            dict_to_write = {'secFromStart': (currentTime - self.start)}

            for element in self.desired_data:
                dict_to_write[element] = inputData[element]

            writer.writerow(dict_to_write)
            """
                'airSpeed' : inputData['airspeed'],
                'altitude' : inputData['altitude'],
                'pitch' : inputData['pitch'],
                'roll' : inputData['roll'],
                'yaw' : inputData['yaw'],
                'xVelocity' : inputData['velocity_x'],
                'yVelocity' : inputData['velocity_y'],
                'zVelocity' : inputData['velocity_z'],
                'voltage' : inputData['voltage']
            """
            return stopWhile
            #This is white the variable in the section titled at the left of the ':'

        self.lastTime = currentTime


if __name__ == '__main__':
    # tempCounter is how many data point to collect temporarily

    theTempCounter = int(input("How long to log in seconds? "))
    x = 0

    my_logger = Logger()

    while x < theTempCounter:  # main loop
        myData = {
            'airspeed' : 1*random.randint(1,10),
            'altitude' : 2*random.randint(1,10),
            'pitch' : 3*random.randint(1,10),
            'roll' : 4*random.randint(1,10),
            'yaw' : 5*random.randint(1,10),
            'velocity_x' : 6*random.randint(1,10),
            'velocity_y' : 7*random.randint(1,10),
            'velocity_z' : 8*random.randint(1,10),
            'voltage' : 9*random.randint(1,10),
        }

        x = my_logger.Update(myData)
        time.sleep(.00001)

    my_logger.exit()
