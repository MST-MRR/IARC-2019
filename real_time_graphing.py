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
    """


    """

    config_filename = 'config.xml'  # Location of configuration file

    max_rows = 3  # Rows of subplots per column

    def __init__(self):
        self.pan_width = 10

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

        self.ani = animation.FuncAnimation(self.fig, self.plot_data, blit=False, interval=20, repeat=False) # interval=10, blit=True, repeat=default

        # Threading
        self.sleep_time = 1e-1

        self.thread_stop = threading.Event()

        self.thread_queue = Queue()

        threads = {
            'reader': threading.Thread(target=self.read_data, args=(self.thread_queue,)),
            'processor': threading.Thread(target=self.process_data, args=(self.thread_queue,))
        }

        for thread in threads.values():
            thread.start()

        self.fig.subplots_adjust(hspace=1, wspace=0.75)  # Avoid subplot overlap

        plt.show()

        self.thread_stop.set()

        for thread in threads.values():
            thread.join()

    def get_demo_data(self):
        """


        """

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

    def read_data(self, q):
        """
        Use: Reads data from network and puts it in a queue to be processed.

        Parameters:
            q: ?
        """

        while not self.thread_stop.is_set():
            data = self.get_demo_data() # This line will change
            q.put(data)
            if (self.data_count > self.plot_count):
                self.sleep_time = self.sleep_time + 1e-5
            elif (self.data_count == self.plot_count):
                self.sleep_time = self.sleep_time - 1e-5
            #print(self.sleep_time)
            sleep(self.sleep_time) # Anything smaller than this time causing trouble

    def process_data(self, q):
        """
        Use: Processes data put into the queue.

        Parameters:
            q: ?
        """
        while not self.thread_stop.is_set():
            try:
                data = q.get(False, self.sleep_time) # Anything smaller than this time causing trouble
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
        """
        Use: Attempts to plot data

        Args:
            frame:

        Returns: Line of each tracked metric
        """

        # If there is no new data to plot, then exit the function.
        if self.plot_count == self.data_count:
            return [metric.get_line for metric in self.tracked_data]


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

        for ax in self.fig.get_axes():
            ax.relim()
            ax.autoscale(axis='y')

            ax.set_xlim(int(self.times[-1]) - self.pan_width, int(self.times[-1]) + self.pan_width)

        self.plot_count += 1

        return [metric.get_line for metric in self.tracked_data]

    @timeit
    def read_config(self):
        """
        Use: To read and interpret the graph config file

        Returns: Dictionary parsed from config file
        """

        root = parse_xml(xxxGrapherxxx.config_filename).getroot()

        graphs = root.findall('graph')

        # Total number of subplots
        count = len(graphs)

        nrows = min(count, xxxGrapherxxx.max_rows)
        ncols = ceil(count / nrows)

        graph_id = 0

        for graph in root.findall('graph'):
            graph_id += 1

            # Make axis
            ax = self.fig.add_subplot(nrows, ncols, graph_id)

            ax.axis([0, 100, 0, 10])

            # Configure the new axis
            ax.set_title(graph.get('title'))
            ax.set_xlabel(graph.get('xlabel'))
            ax.set_ylabel(graph.get('ylabel'))

            for metric in graph.findall('metric'):
                output = metric.get('output') if metric.get('output') else 'graph'

                if output == 'text':
                    ax.text(0, 0, metric.get('func'), fontsize=12)

                elif output == 'graph':
                    m_line, = ax.plot([], [], color=metric.get('color'), label=metric.get('label'))

                    # TODO - [met.text for met in metric.findall('data_stream')]

                    self.tracked_data.append(Metric(m_line, metric.get("func"), metric.get('data_stream')))

            ax.legend()


if __name__ == '__main__':
    test_object = xxxGrapherxxx()
