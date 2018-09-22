import threading
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import pause
import matplotlib.animation as animation

# Thid function is purely for testing purposes and
# will be replaced by whatever mechanism gets data
# from the socket
def fromSocket():
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


def get_data():
    # Collect data coming in from network socket
    global data
    global times
    new_data = fromSocket()
    times.append(time.time())
    for keyword in tracked_data:
        data[keyword].append(new_data[keyword])
    # Chose 0.01 because data (under ideal conditions) 
    # will be coming in from socket at this speed
    pause(0.01)
    

def plot_data(frame, ax):
    # Plot data coming in
    global data
    global times
    get_data()
    for line in ax.get_lines():
        line.set_data(times, data[line.get_label()])
    return ax.get_lines()


def read_config():
    # Reads the config file and stores the resulting
    # graphs in desired_graphs
    pass

def make_subplots():
    # Makes subplots according to configure information
    pass

# Stores graph information
class Graph():
    def __init__(self, **kwargs):
        # TODO
        pass

# Initialize values to be used

# Stores times corresponding to each data index
times = []

# All the possible data values that cann be pulled from the
# data stream. 
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

#tracked_data = []
tracked_data = ['pitch', 'roll', 'yaw']

start_time = time.time()

fig = plt.figure()

read_config()

make_subplots()

ax = fig.subplots()
ax.plot([], [], 'r-', color="blue", label="pitch")
ax.plot([], [], 'r-', color="red", label="yaw")
ax.plot([], [], 'r-', color="green", label="roll")

plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xlabel('x')
plt.title('test')

line_ani = animation.FuncAnimation(fig, plot_data, None, fargs=(ax,),
                                   interval=10, blit=True)

plt.show()

#threading.Thread(target=get_data).start()
#threading.Thread(target=plot_data).start()


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