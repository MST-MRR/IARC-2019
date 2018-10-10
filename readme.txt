The grapher manages 1+ individual metrics which are just things that take in specific data streams and process them to
be displayed on the graph. The metrics can be displayed on different graphs but the processing is done on a per metric
basis. Data comes in through read_data which pulls whatever new data has come in from the drone. That data is then sent
to whichever metrics requested specific data streams and the processed data is saved in the metric's data list. The data
in the metric's data list is what will be graphed. These three functions, read, process and plot, all happen
concurrently in multiple threads that start when the others are 'sleeping'.

When creating a grapher object there is 2 optional parameters:
    pan_width: (int, default 10) Time in seconds to display graph in the past. This is essentially the x limit.
    y_lim: (tuple(int, int), default (0, 10)) The

To interface with the grapher, you need to edit the config.xml file(In the future a GUI will edit the xml for you).
Everything that you want the grapher to read should be within the 'desiredgraphs' tag meaning after <desiredgraphs> and
before </desiredgraphs>. Each subplot(Must be at least 1) is denoted with a <graph> tag. These subplots hold the
individual metrics that take in and process the data.
Subplot settings:
    title: (optional) The title of the graph.
    output: (optional) If output is set to 'text', every metric will be displayed at bottom in text form(should only be
                        one of these at a time.
    xlabel: (optional) The x axis label.
    ylabel: (optional) The y axis label.
    legend: (optional, default='yes') Whether or not to display a legend on the subplot, must be yes to make true.

Metric settings:
    line: Either the animation line or a piece of text.
    label: (optional, taken from line if is one) Title of metric that appears on legend.
    func: Function to generate data for graph. Can use variables x, y, z(if a data stream is set for that variable).
            Can make use of primitive python math functions ie +, -, *, /, (), max, min... To use boolean must TODO -------------------------------------- >< dont work and must use is
    x_stream: (optional) The data stream to be sent to x variable.
    y_stream: (optional) The data stream to be sent to y variable(x variable must be set first!).
    z_stream: (optional) The data stream to be sent to z variable(x & y variables must be set first!).
    color: (optional) Matplotlib standard colors or hex(#FFFFFF) color value. Can set color or have generated on per
            subplot basis. Color generator currently only can generate 6 unique colors so if you have more than 6
            metrics on a plot you may need to manually set colors.

Your choices of data_streams are:
    'roll', 'pitch', 'yaw', 'target_altitude', 'target_roll_velocity',
    'target_pitch_velocity', 'altitude', 'airspeed', 'velocity_x', 
    'velocity_y', 'velocity_z', 'voltage', 'state', 'mode',
    'armed', 'altitude_controller_output', 'altitude_rc_output', 
    'pitch_controller_output', 'pitch_rc_output', 'roll_controller_output', 
    'roll_rc_output', 'yaw_controller_output', 'yaw_rc_output', 
    'target_yaw', 'color_image', 'depth_image'
