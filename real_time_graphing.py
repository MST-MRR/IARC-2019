import threading
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import pause
import matplotlib.animation as animation
import xml.etree.ElementTree as ET  # https://www.geeksforgeeks.org/xml-parsing-python/

# ---------------------------------------------
# Functions (core logic)
# ---------------------------------------------

# Thid function is purely for testing purposes and
# will be replaced by whatever mechanism gets data
# from the socket
def from_socket():
    gen = np.random.rand(26, 1)
    imaginary_data = {
        'altitude': gen[0, 0],
        'airspeed': gen[1, 0],
        'velocity_x': gen[2, 0],
        'velocity_y': gen[3, 0],
        'velocity_z': gen[4, 0],
        'voltage': gen[5, 0],
        'state': gen[6, 0],
        'mode': gen[7, 0],
        'armed': gen[8, 0],
        'roll': gen[9, 0],
        'pitch': gen[10, 0],
        'yaw': gen[11, 0],
        'altitude_controller_output': gen[12, 0],
        'altitude_rc_output': gen[13, 0],
        'target_altitude': gen[14, 0],
        'pitch_controller_output': gen[15, 0],
        'pitch_rc_output': gen[16, 0],
        'target_pitch_velocity': gen[17, 0],
        'roll_controller_output': gen[18, 0],
        'roll_rc_output': gen[19, 0],
        'target_roll_velocity': gen[20, 0],
        'yaw_controller_output': gen[21, 0],
        'yaw_rc_output': gen[22, 0],
        'target_yaw': gen[23, 0],
        'color_image': gen[24, 0],
        'depth_image': gen[25, 0]
    }
    return imaginary_data

"""
def get_data():
    # Collect data coming in from network socket
    global data
    global times
    global start_time
    new_data = from_socket()
    times.append(time.time() - start_time)
    for item in tracked_data:
        t = item.get_title()
        data[t].append(new_data[t])
"""
    
def plot_data(frame, fig):
    # Plot data coming in
    #global data
    global times
    global start_time
    global check_time

    # Used to determine whether to pan or not
    flag = False

    data = from_socket()
    times.append(time.time() - start_time)

    for metric in tracked_data:
        func = metric.get_func()
        x_val = func(data[metric.get_data_label()])
        new_data = metric.push_data(x_val)

        metric.get_line().set_data(np.asarray(times), np.asarray(new_data))

    # See if it is time to pan
    now = time.time()
    if now - check_time > 5: 
        flag = True
        check_time = now

    for ax in fig.get_axes():
        ax.relim()
        ax.autoscale(axis='y')
        if flag:
            # Pan
            most_current_time = times[-1]
            ax.set_xlim(left=most_current_time - 1, right=most_current_time + 6) 
        

    return [metric.get_line() for metric in tracked_data]


def read_config(fig):
    # Reads the config file and stores the resulting
    # graphs in desired_graphs
    """
    Use: To read and interpret the graph config file

    Returns: Dictionary parsed from config file
    """

    # XML file structure
    """
    root
        Data:
            x: 1
            y: 2

    Currently only desired graphs
        Desired Graphs
            Graph: Title, x_label, y_label
                Metrics
                    Metric: Title, function
                    Metric: Title, function
                    
            Graph: Title, x_label, y_label
                Metrics
                    Metric: Title, funciton
    """

    global tracked_data
    global config_filename

    # Get root
    root = ET.parse(config_filename).getroot()

    graphs = root.findall('graph')

    nrows = 3
    count = len(graphs)
    ncols = int(count / nrows) + 1

    index = 1
    for graph in root.findall('graph'):
        title = graph.get('title')
        # Make axis
        ax = fig.add_subplot(nrows, ncols, index)
        index = index + 1
        ax.set_title(title)
        ax.set_xlabel(graph.get('xlabel'))
        ax.set_ylabel(graph.get('ylabel'))
        ax.set_xlim(left=0, right=7)

        for metric in graph.findall('metric'):
            # Make 2DLine
            line, = ax.plot([], [], color=metric.get('color'), label=metric.get('title'))
            func = metric.get('func')
            newMetric = Metric(line, func, title)
            tracked_data.append(newMetric)

"""
def make_subplots(fig):
    # Makes subplots according to configure information
    nrows = 3
    count = len(tracked_data)
    ncols = int(count / nrows)

    index = 1
    for item in tracked_data:
        # Make axis
        ax = fig.add_subplot(nrows, ncols, index)
        ax.set_label(item.get_title())
        index = index + 1
        for metric in item.get_metrics():
            line = ax.plot([], [], color=metric.get_color(), label=metric.get_title()
"""

"""
# Wraps around Axis object
class Graph():
    def __init__(self):
        self.lines = []
        self.metrics = []
        pass

    def set_title(self, title):
        self.ax.set_title(title)

    def get_title(self):
        return self.ax.get_title()

    def set_xlabel(self, xlabel):
        self.ax.set_xlabel(xlabel)

    def get_xlabel(self):
        return self.ax.get_xlabel()

    def set_ylabel(self, ylabel):
        self.ax.set_ylabel(ylabel)

    def get_ylabel(self):
        return self.ax.get_ylabel()

    def append_metric(self, line, func):
        newMetric = Metric(line, func)
        self.metrics.append(newMetric)
"""

# Wraps around 2DLine object
class Metric():
    def __init__(self, line, func, data_label):
        self.line = line
        self.data_label = data_label
        self.func = lambda x: eval(func)
        self.data = []

    def set_data_label(self, data_label):
        self.data_label = data_label

    def get_data_label(self):
        return self.data_label

    def get_func(self):
        return self.func

    def get_line(self):
        return self.line

    def push_data(self, data_point):
        self.data.append(data_point)
        return self.data

    def get_data(self):
        return self.data

# Initializes figure for graphing
def init():
    global ax
    

# ---------------------------------------------
# Initialize values to be used
# ---------------------------------------------

# Location of configuration file
config_filename = 'config.xml'

# Stores times corresponding to each data index
times = []

# Stored which data items we are interested in
tracked_data = []

# All the possible data values that cann be pulled from the
# data stream. 
"""
data = {
    'altitude': [],
    'airspeed': [],
    'velocity_x': [],
    'velocity_y': [],
    'velocity_z': [],
    'voltage': [],
    'state': [],
    'mode': [],
    'armed': [],
    'roll': [],
    'pitch': [],
    'yaw': [],
    'altitude_controller_output': [],
    'altitude_rc_output': [],
    'target_altitude': [],
    'pitch_controller_output': [],
    'pitch_rc_output': [],
    'target_pitch_velocity': [],
    'roll_controller_output': [],
    'roll_rc_output': [],
    'target_roll_velocity': [],
    'yaw_controller_output': [],
    'yaw_rc_output': [],
    'target_yaw': [],
    'color_image': [],
    'depth_image': []
}
"""

# ---------------------------------------------
# Set up figure and start animating
# ---------------------------------------------

fig = plt.figure()

read_config(fig)

fig.subplots_adjust(hspace=1)

start_time = time.time()
check_time = start_time

line_ani = animation.FuncAnimation(fig, plot_data, fargs=(fig,),
                                   interval=10, blit=True)

plt.show()

#threading.Thread(target=get_data).start()
#threading.Thread(target=plot_data).start()
