import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.pyplot import pause
import xml.etree.ElementTree as ET  # https://www.geeksforgeeks.org/xml-parsing-python/
import threading

from timer import timeit

# Utility
import time
from math import ceil

# User-defined
from metric import Metric


class xxxGrapherxxx:
    def __init__(self):
        # How often to redraw xlims (Redrawing xlims is expensive)
        self.pan_width = 10

        # Stored which data items we are interested in
        self.tracked_data = []

        self.plot_count = 0
        self.data_count = 0

        # Stores times corresponding to each data index
        self.times = []

        self.check_time = self.start_time = time.time()

        # Initializes figure for graphing
        self.fig = plt.figure()
        for ax in self.fig.get_axes():
            # Set xlims so that initial data is seen coming in
            ax.set_xlim(left=0, right=pan_width + 1)

        # Avoid subplot overlap
        self.fig.subplots_adjust(hspace=1, wspace=0.75)

        self.read_config()

        line_ani = animation.FuncAnimation(self.fig, self.plot_data,  # init_func=init, fargs=(self.fig,)
                                           interval=10, blit=True)

        plt.show()

        # return [metric.get_line() for metric in self.tracked_data]

    # ---------------------------------------------
    # Functions (core logic)
    # ---------------------------------------------

    # Thid function is purely for testing purposes and
    # will be replaced by whatever mechanism gets data
    # from the socket
    def from_socket(self):
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

    # This function is not currently being called
    def get_data(self):
        # Should be a dictionary exactly like imaginary_data
        new_data = from_socket()
        # This line should run as closely as possible to
        # when data is added to each metric
        self.times.append(time.time() - self.start_time)
        for metric in self.tracked_data:
            func = metric.get_func()
            x_val = func(new_data[metric.get_data_stream()])
            metric.push_data(x_val)
        self.data_count += 1

    @timeit
    def plot_data(self, frame):

        """
        if plot_count == data_count:
            return [metric.get_line() for metric in tracked_data]
        """

        # Used to determine whether to pan or not
        flag = False

        # This will eventually happen in get_data.
        # The reason it isn't right now is because
        # we are unsure of how to run get_data in
        # a separate thread.
        data = self.from_socket()
        self.times.append(time.time() - self.start_time)

        for metric in self.tracked_data:
            # Ideally, this will also happen in get_data so
            # that there is nothing to bottleneck drawing speed
            func = metric.get_func()
            x_val = func(data[metric.get_data_stream()])
            new_data = metric.push_data(x_val)

            metric.get_line().set_data(np.asarray(self.times), np.asarray(new_data))

        # See if it is time to pan
        now = time.time()
        if now - self.check_time > self.pan_width:
            flag = True
            self.check_time = now

        for ax in self.fig.get_axes():
            ax.relim()
            ax.autoscale(axis='y')
            if flag:
                # Pan
                most_current_time = self.times[-1]
                ax.set_xlim(left=most_current_time - 1, right=most_current_time + self.pan_width + 1)
                # This is an expensive call, but must be made if we want to
                # update tick marks. See https://bit.ly/2OLAlJH
                #fig.canvas.draw()

        self.plot_count += 1
        return [metric.get_line() for metric in self.tracked_data]

    def read_config(self):
        # Reads the config file makes subplots
        """
        Use: To read and interpret the graph config file

        Returns: Dictionary parsed from config file
        """
        global config_filename

        # Get root
        root = ET.parse(config_filename).getroot()

        graphs = root.findall('graph')

        # Constant value - do not change
        max_rows = 3

        # Used to determine where to put each subplot
        c = 0
        r = 0

        # Total number of subplots
        count = len(graphs)

        nrows = min(count, max_rows)
        ncols = ceil(count / nrows)

        for graph in root.findall('graph'):
            title = graph.get('title')
            # Determine where this subplot should go
            index = (ncols*c) + r + 1
            # Make axis
            ax = self.fig.add_subplot(nrows, ncols, index)
            # Keep track of where next subplot should go
            c = c + 1
            if c / max_rows == 1:
                c = 0
                r = r + 1
            # Configure the new axis
            ax.set_title(title)
            ax.set_xlabel(graph.get('xlabel'))
            ax.set_ylabel(graph.get('ylabel'))
            ax.set_xlim(left=0, right=7)

            for metric in graph.findall('metric'):
                # Make 2DLine
                m_color = metric.get('color')
                m_label = metric.get('label')
                m_data_stream = metric.get('data_stream')
                m_func = metric.get('func')
                m_line, = ax.plot([], [], color=m_color, label=m_label)
                newMetric = Metric(m_line, m_func, m_label, m_data_stream)
                self.tracked_data.append(newMetric)


if __name__ == '__main__':
    # ---------------------------------------------
    # Initialize values to be used
    # ---------------------------------------------

    # Location of configuration file
    config_filename = 'config.xml'

    # XML file structure
    """
    <desiredgraphs>
        <graph title="" xlabel="" ylabel="">
            <metric label="" data_stream="" func="" color=""></metric>
            ...
            <metric label="" data_stream="" func="" color=""></metric>
        </graph>
        ...
        <graph title="" xlabel="" ylabel="">
            <metric label="" data_stream="" func="" color=""></metric>
            ...
            <metric label="" data_stream="" func="" color=""></metric>
        </graph>
    </desiredgraphs>
    """

    test_object = xxxGrapherxxx()

    # ---------------------------------------------
    # Set up figure and start animating
    # ---------------------------------------------

    """
    while True:
        print ("got here")
        get_data()
        pause(0.5)
    """

    #threading.Thread(target=get_data).start()
    #threading.Thread(target=plot_data).start()

