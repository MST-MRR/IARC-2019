# Logging IARC-2019
Real time logging for the drone, can work on board or over network.

## Configuration
When a Logger object is created, the desired_data parameter should be set to a list of keys to look for in the received
data. Since data is sent to the logger in the form of a dictionary, desired_data should be a list of keys present so
that it can pull relevant data.

The filename to save the log file to will automatically be chosen. There should be a __'generated_logs'__
file in tools/

## Operating

Once the logger object is created, __Logger.update()__ can be called to pass
in data. The time that the logger receives the data is the time that
gets logged. Any data that should be logged for should have its key in the desired_data list on logger creation.

Data should be passed into the update function in the format
    
    {key(str): data(number)}
    
When done, the logger.exit() function should be called.

__Only__ the headers in desired data(set in constructor) will be logged!

## Troubleshooting
If you have issues or suggestions, message Cole Dieckhaus or Jon Ogden on slack.