import numpy as np

import matplotlib.pyplot as plt

import matplotlib.animation as animation

from xml.etree.ElementTree import parse as parse_xml

import threading

from multiprocessing import Queue

import queue

from time import sleep

# Utility
from time import time
from timer import timeit
from math import ceil

# User-defined
from metric import Metric


class xxxGrapherxxx:
    # Location of configuration file
    config_filename = 'config.xml'

    # Constant value - do not change
    max_rows = 3

    def __init__(self):
        # How often to redraw xlims (Redrawing xlims is expensive)
        self.pan_width = 10

        self.stop = threading.Event()

        self.q = Queue()

        # Stored which data items we are interested in
        self.tracked_data = []

        self.plot_count = 0
        self.data_count = 0

        # Stores times corresponding to each data index
        self.times = []

        self.check_time = self.start_time = time()

        # Initializes figure for graphing
        self.fig = plt.figure()

        self.read_config()

        reader_thread = threading.Thread(target=self.read_data, args=(self.q,))
        processor_thread = threading.Thread(target=self.process_data, args=(self.q,))

        line_ani = animation.FuncAnimation(self.fig, self.plot_data,   # init_func=init, fargs=(self.fig,)
                                           interval=10, blit=True)

        reader_thread.start()
        processor_thread.start()

        for ax in self.fig.get_axes():
            # Set xlims so that initial data is seen coming in
            ax.set_xlim(left=0, right=self.pan_width + 1)

        # TODO - set pan width

        # Avoid subplot overlap
        self.fig.subplots_adjust(hspace=1, wspace=0.75)

        plt.show()

        self.stop.set()

        #for thread in threads:
         #   thread.join()

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

    # Reads data from network and puts it in a queue to be processed.
    def read_data(self, q):
        while not self.stop.is_set():
            data = self.from_socket() # This line will change
            q.put(data)
            sleep(1e-1) # Anything smaller than this time causing trouble

    # Processes data put into the queue.
    def process_data(self, q):
        while not self.stop.is_set():
            try:
                data = q.get(False, 1e-1) # Anything smaller than this time causing trouble
                self.times.append(time() - self.start_time)
                for metric in self.tracked_data:
                    func = metric.get_func
                    x_val = func(data[metric.get_data_stream])
                    metric.push_data = x_val
                self.data_count += 1
            except queue.Empty:
                pass

    @timeit
    def plot_data(self, frame):

        # If there is no new data to plot, then exit the function.
        # Note: the 0ms times come when this condition is met.
        if self.plot_count == self.data_count:
            return [metric.get_line for metric in self.tracked_data]

        # Used to determine whether to pan or not
        flag = False

        """
        # This will eventually happen in get_data.
        # The reason it isn't right now is because
        # we are unsure of how to run get_data in
        # a separate thread.
        data = self.from_socket()
        self.times.append(time() - self.start_time)
        """

        for metric in self.tracked_data:
            """
            # Ideally, this will also happen in get_data so
            # that there is nothing to bottleneck drawing speed
            func = metric.get_func()
            x_val = func(data[metric.get_data_stream()])
            new_data = metric.push_data(x_val)
            """

            metric.get_line.set_data(np.asarray(self.times), np.asarray(metric.get_data))

        # See if it is time to pan
        now = time()
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

                # update tick marks. See https://bit.ly/2OLAlJH
                # fig.canvas.draw()  # This is an expensive call, but must be made if we want to

        self.plot_count += 1
        return [metric.get_line for metric in self.tracked_data]

    def read_config(self):
        """
        Use: To read and interpret the graph config file

        Returns: Dictionary parsed from config file
        """

        root = parse_xml(xxxGrapherxxx.config_filename).getroot()

        graphs = root.findall('graph')

        # Used to determine where to put each subplot

        # Total number of subplots
        count = len(graphs)

        nrows = min(count, xxxGrapherxxx.max_rows)
        ncols = ceil(count / nrows)

        i = 0

        for graph in root.findall('graph'):
            i+=1

            #column = int(count / xxxGrapherxxx.max_rows) + 1
            #row = count % xxxGrapherxxx.max_rows + 1

            # Determine where this subplot should go
            #index = (ncols*column) + row + 1
            # Make axis
            ax = self.fig.add_subplot(nrows, ncols, i)

            """
            # Keep track of where next subplot should go
            column += 1
            if column / xxxGrapherxxx.max_rows == 1:
                column = 0
                row += 1"""

            # Configure the new axis
            ax.set_title(graph.get('title'))
            ax.set_xlabel(graph.get('xlabel'))
            ax.set_ylabel(graph.get('ylabel'))
            ax.set_xlim(left=0, right=7)

            for metric in graph.findall('metric'):
                # Make 2DLine
                m_line, = ax.plot([], [], color=metric.get('color'), label=metric.get('label'))

                self.tracked_data.append(Metric(m_line, metric.get('func'), metric.get('data_stream')))


if __name__ == '__main__':
    test_object = xxxGrapherxxx()

    
