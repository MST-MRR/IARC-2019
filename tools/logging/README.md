# Logging IARC-2019
Real time logging for the drone, can work on board or over network.

## Configuration
When a Logger object is created a dictionary consisting of 
{header: data stream} pairs can be passed in or default settings are
used.

A data stream is a stream of data as it comes in from the drone.

Possible Data streams:
    
    'roll', 'pitch', 'yaw', 'target_altitude', 'target_roll_velocity',
    'target_pitch_velocity', 'altitude', 'airspeed', 'velocity_x', 
    'velocity_y', 'velocity_z', 'voltage', 'state', 'mode',
    'armed', 'altitude_controller_output', 'altitude_rc_output', 
    'pitch_controller_output', 'pitch_rc_output', 'roll_controller_output', 
    'roll_rc_output', 'yaw_controller_output', 'yaw_rc_output', 
    'target_yaw', 'color_image', 'depth_image'

The filename to save the log file to will automatically be chosen.

## Operating

Once the logger object is created Logger.update() can be called to pass
in data. The time that the logger receives the data is the time that
gets logged.

Data should be passed into the update function in the format
    
    {header: data}
    
When done, the logger.exit() function should be called.


## Troubleshooting
If you have issues or suggestions, message Cole Dieckhaus or Jon Ogden on slack or email cole - csdhv9@mst.edu.