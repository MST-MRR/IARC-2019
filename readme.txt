<!--
Your choices of data_streams are:
    'roll', 'pitch', 'yaw', 'target_altitude', 'target_roll_velocity',
    'target_pitch_velocity', 'altitude', 'airspeed', 'velocity_x', 
    'velocity_y', 'velocity_z', 'voltage', 'state', 'mode',
    'armed', 'altitude_controller_output', 'altitude_rc_output', 
    'pitch_controller_output', 'pitch_rc_output', 'roll_controller_output', 
    'roll_rc_output', 'yaw_controller_output', 'yaw_rc_output', 
    'target_yaw', 'color_image', 'depth_image'
-->

<!--
Metric has a func attribute which is run on each incoming data stream.
IMPORTANT: If you just want to plot the data coming in as is, the function should
be set to 'x', indicating a one-to-one relationship between input and output.
-->