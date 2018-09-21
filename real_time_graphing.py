import threading
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



def get_data():
    # Collect data coming in from network socket
    pass

def plot_data():
    # Plot data coming in
    pass

def read_config():
    # Reads the config file and stores the resulting
    # graphs in desired_graphs
    pass

def make_sub_plots():
    # Makes subplots according to configure information
    pass

# Stores graph information
class Graph():
    def __init__(self, **kwargs):
        # TODO

# Initialize values to be used

# All the possible data values that cann be pulled from the
# data stream. 
data = {
    'altitude': [],
    'airspeed': []],
    'velocity_x': [],
    'velocity_y': []],
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

desired_graphs = []

start_time = timetime()

fig = plt.figure()

read_config()

make_subplots()

threading.Thread(target=get_data).start()
threading.Thread(target=plot_data).start()


# Graphing test program to be incorporated
"""
def update_line(num, data, ax):
    for line in ax.get_lines():
        gen = np.random.rand(2, 50)
        data[0] = gen[0, :]
        data[1] = gen[1, :]
        line.set_data(np.asarray(data)[:, :])
    return ax.get_lines()

# Fixing random state for reproducibility
np.random.seed(19680801)


ax = fig.subplots()
ax.plot([], [], 'r-', color="blue")
ax.plot([], [], 'r-')
ax.plot([], [], 'r-', color="green")

plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xlabel('x')
plt.title('test')
line_ani = animation.FuncAnimation(fig, update_line, None, fargs=(data, ax),
                                   interval=10, blit=True)
plt.show()
"""