import numpy as np
from matplotlib import pyplot as plt, animation as animation

from xml.etree.ElementTree import parse as parse_xml

import threading
from multiprocessing import Queue
import queue

from time import sleep, time

from metric import Metric


def get_demo_data():
    """
    Generates random data in the format the grapher will receive data.

    Returns
    -------
    dict
        Keys of data streams w/ randomly generated data.
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


class RealTimeGraph:
    """
    Description

    Parameters
    ----------
    pan_width: int
        Time in seconds to display previous data

    Raises
    ------
    ?
    """

    config_filename = 'config.xml'  # Location of configuration file

    max_rows = 3  # Rows of subplots per column

    data_freq_warning = .5  # If time values are this far apart warn the user

    def __init__(self, pan_width=10):

        self.pan_width = abs(pan_width)

        # Stored which data items we are interested in
        self.tracked_data = []

        self.plot_count = 0
        self.data_count = 0

        # Stores times corresponding to each data index
        self.times = []

        self.check_time = self.start_time = time()

        # Initializes figure for graphing
        self.fig = plt.figure(figsize=(8, 6))
        self.fig.canvas.set_window_title('Real Time Graphing')

        self.parse_config()

        self.ani = animation.FuncAnimation(self.fig, self.plot_data, blit=False, interval=20, repeat=False)

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

        #
        # Code stops here until matplot window closed
        plt.show()

        #
        # Cleanup
        self.thread_stop.set()

        for thread in threads.values():
            thread.join()

    def parse_config(self):
        """
        Reads and interprets the graph config file

        Returns
        -------
        dict
            Parsed config file
        """

        root = parse_xml(RealTimeGraph.config_filename).getroot()

        # Total number of subplots
        graph_count = [graph.get("output") == 'text' for graph in root.findall('graph')].count(False)

        nrows = min(graph_count, RealTimeGraph.max_rows)
        ncols = int(graph_count / nrows) + (graph_count % nrows > 0)

        def unique_color_generator(colors_taken):
            color_list = ['blue', 'orange', 'red', 'green', 'yellow', 'black', 'Ran out of colors!']

            seen = set(colors_taken)

            for elem in color_list:
                if elem not in seen:
                    yield elem
                    seen.add(elem)

        for graph in root.findall('graph'):
            if graph.get('output') == 'text':
                i = 0
                for metric in graph.findall('metric'):
                    # Coords are percent
                    text = ax.text(i * (1 / len(graph.findall('metric'))), 0, 'matplotlib', transform=plt.gcf().transFigure)

                    self.tracked_data.append(Metric(line=text, label=metric.get('label'), xml_tag=metric))
                    i += 1

            else:
                color_gen = unique_color_generator([metric.get('color') for metric in graph.findall('metric')])

                # Make axis
                ax = self.fig.add_subplot(nrows, ncols, len(self.fig.get_axes()) + 1)

                ax.axis([0, 100, 0, 10])

                # Configure the new axis
                ax.set_title(graph.get('title'))
                ax.set_xlabel(graph.get('xlabel'))
                ax.set_ylabel(graph.get('ylabel'))

                for metric in graph.findall('metric'):
                    color = metric.get('color') if metric.get('color') else next(color_gen)

                    m_line, = ax.plot([], [], color=color, label=metric.get('label'))

                    self.tracked_data.append(Metric(line=m_line, xml_tag=metric))

                if (graph.get('legend') if graph.get('legend') else 'yes') == 'yes':
                    ax.legend()

    def read_data(self, thread_queue):
        """
        Reads data from network and puts it in a queue to be processed.

        Parameters
        ----------
        thread_queue: Thread queue
            Thread queue
        """

        while not self.thread_stop.is_set():
            data = get_demo_data()
            thread_queue.put(data)

            # Adjust sleep times
            if self.data_count > self.plot_count:
                self.sleep_time = self.sleep_time + 1e-5

            elif self.data_count == self.plot_count:
                self.sleep_time = self.sleep_time - 1e-5

            sleep(self.sleep_time)

    def process_data(self, thread_queue):
        """
        Processes data put into the queue.

        Parameters
        ----------
        thread_queue: Thread queue
            Thread queue
        """

        while not self.thread_stop.is_set():
            try:
                data = thread_queue.get(False, self.sleep_time)

                self.times.append(time() - self.start_time)

                # Checks data frequency to see if poor quality
                try:
                    if self.times[-1] > self.times[-2] + RealTimeGraph.data_freq_warning:
                        print("Data quality: Sucks")
                except IndexError:
                    pass

                for metric in self.tracked_data:
                    func = metric.get_func

                    x = data[metric.get_x_stream] if metric.get_x_stream else None
                    y = data[metric.get_y_stream] if metric.get_y_stream else None
                    z = data[metric.get_z_stream] if metric.get_z_stream else None

                    x_val = func(x, y, z) if z else (func(x, y) if y else func(x))

                    metric.push_data = x_val
                self.data_count += 1
            except queue.Empty:
                pass

    def plot_data(self, frame):
        """
        Plots data

        Parameters
        ----------
        frame:
            Arbitrary variable, animation function sends frame in by default.

        Returns
        -------
        list
            Line of each tracked metric

        """

        # If there is no new data to plot, then exit the function.
        if self.plot_count == self.data_count:
            return [metric.get_line for metric in self.tracked_data]

        for metric in self.tracked_data:
            try:
                metric.get_line.set_data(np.asarray(self.times), np.asarray(metric.get_data))
            except AttributeError:
                metric.get_line.set_text("{}: {}".format(metric.get_label, str(metric.get_data[-1])[:5]))

        for ax in self.fig.get_axes():
            try:
                ax.relim()
                ax.autoscale(axis='y')
            except ValueError as e:
                print("Caught '{}'!\nPast 10 times: {}\nPast 10 outputs: {}".format(e, self.times[-10:], metric.get_data[-10:]))

            current_time = int(self.times[-1])

            ax.set_xlim(current_time - self.pan_width, current_time + self.pan_width)

        self.plot_count += 1

        return [metric.get_line for metric in self.tracked_data]


if __name__ == '__main__':
    test_object = RealTimeGraph()
