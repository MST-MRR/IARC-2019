#this is for defining the gloabal variables used in the Logging files
import time

def init():

    global date 
    date = time.strftime('%x') #Gets todays date

    global newDate 
    newDate = date.replace('/','_') #changes the / for _ to not mess us the directory

    global directory 
    directory = 'C:/Users/jonat/Desktop/MultiRotor_Logging/' #where we will save all logs - folder name - can be changed

    global fileName1
    fileName1 = newDate #part 1 modified date

    global fileName2
    fileName2 = "_Flight_Num_" #part 2 - string that stays the same

    global fileName3
    fileName3 = input("What flight number is this flight (numbering restarts each day)? ")
    #Above prompts for the flight number so there can be seperate files for each flight that day

    global endLoop
    endLoop = int(input("How many data values to store? ")) #this variable will have to be something the keeps
    #The loop running until the flight ends - this is for testing
    directory = directory + fileName1 + fileName2 + fileName3 #final directory path

    global airSpeed
    airSpeed = directory + "/" + newDate + "_AirSpeedLogging"+ fileName3 + '.csv'

    global altitude
    altitude = directory + "/" + newDate + "_AltitudeLogging"+ fileName3 + '.csv'

    global pitch
    pitch = directory + "/" + newDate + "_PitchLogging"+ fileName3 + '.csv'

    global roll
    roll = directory + "/" + newDate + "_RollLogging"+ fileName3 + '.csv'

    global xVelocity
    xVelocity = directory + "/" + newDate + "_Velocity_xLogging"+ fileName3 + '.csv'

    global yVelocity
    yVelocity = directory + "/" + newDate + "_Velocity_yLogging"+ fileName3 + '.csv'

    global zVelocity
    zVelocity = directory + "/" + newDate + "_Velocity_zLogging"+ fileName3 + '.csv'

    global voltage
    voltage = directory + "/" + newDate + "_VoltageLogging"+ fileName3 + '.csv'

    global yaw
    yaw = directory + "/" + newDate + "_YawLogging"+ fileName3 + '.csv'

    global start
    start = time.time()