
import os
import time
import shutil

#this imports the required files
import SettingsLogging
import AltitudeLogging
import AirSpeedLogging
import Velocity_xLogging
import Velocity_yLogging
import Velocity_zLogging
import VoltageLogging
import RollLogging
import PitchLogging
import YawLogging

SettingsLogging.init()

if not os.path.exists(SettingsLogging.directory): #checks to see if the path already exists
   os.makedirs(SettingsLogging.directory) #if it doesn't exist it makes it
    
masterDirectory = 'C:/Users/jonat/Desktop/Master_Logging'

#This section will intialize all the logging files

AltitudeLogging.init()
AirSpeedLogging.init()
Velocity_xLogging.init()
Velocity_yLogging.init()
Velocity_zLogging.init()
VoltageLogging.init()
RollLogging.init()
PitchLogging.init()
YawLogging.init()

#This while loop logs the data in order they are presented until it is satisfied
i = 0
while i < SettingsLogging.endLoop:
    AltitudeLogging.run()
    AirSpeedLogging.run()
    Velocity_xLogging.run()
    Velocity_yLogging.run()
    Velocity_zLogging.run()
    VoltageLogging.run()
    RollLogging.run()
    PitchLogging.run()
    YawLogging.run()
    i+=1
 

