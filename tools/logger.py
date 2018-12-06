import time
import csv
import os


class Logger:
    """
    Object that can be sent data to be logged

    Run Requirements: Must be run from base folder or in tools folder!

    Version: python 2.7 / 3.6(Best)

    Parameters
    ----------
    desired_data: dict
        Pair of headers and data streams. Time is set as first header by default.
    """
    def __init__(self, desired_data=None):

        #
        # Setup dict w/ headers matched to desired data stream
        self.desired_data = {'secFromStart': None}
        self.desired_data.update(
            {'airspeed': 'airspeed',  'altitude': 'altitude', 'pitch': 'pitch', 'roll': 'roll', 'yaw': 'yaw',
             'velocity_x': 'velocity_x', 'velocity_y': 'velocity_y', 'velocity_z': 'velocity_z', 'voltage': 'voltage'}
            if not desired_data else desired_data)

        #
        # Setup directory name
        date = time.strftime('%x').replace('/', '_')  # Gets today's date & sets / to _ as not mess up the directory

        file_name_start = '{}_Flight_Num_'.format(date)

        # generated logs file to always save to
        resource_file_dir = "generated_logs/"

        if 'tools' in os.listdir("."):
            resource_file_dir = "tools/" + resource_file_dir

        prev_flight_num = 0 if not os.listdir(resource_file_dir) else max([int(element.split(file_name_start)[1].split('.csv')[0]) if file_name_start in element else 0 for element in os.listdir(resource_file_dir)])
        daily_flight = prev_flight_num + 1

        self.directory = '{}{}{}.csv'.format(resource_file_dir, file_name_start, str(daily_flight))

        #
        # Create file
        self.logging_file = open(self.directory, "w")

        self.writer = csv.DictWriter(self.logging_file, fieldnames=self.desired_data.keys())

        self.writer.writeheader()

        #
        # Init timing variables
        self.start_time = time.time()
        self.last_update_time = 0

    def exit(self):
        """
        Closes file that was logging data.
        """

        self.logging_file.close()

    def update(self, input_data):
        """
        Log data to file.

        Parameters
        ----------
        input_data: dict
            Stream of new data to be logged
        """

        current_time = time.time()

        if self.last_update_time != current_time:
            self.writer.writerow({key: input_data[element] if element else current_time - self.start_time for key, element in self.desired_data.items()})

        self.last_update_time = current_time


if __name__ == '__main__':
    import math

    # tempCounter is how many data point to collect temporarily

    theTempCounter = int(input("How long to log in seconds? "))

    stopWhile = 0

    my_logger = Logger({'airspeed': 'airspeed',  'altitude': 'altitude', 'pitch': 'pitch', 'roll': 'roll', 'yaw': 'yaw',
             'velocity_x': 'velocity_x', 'velocity_y': 'velocity_y', 'velocity_z': 'velocity_z',
            'voltage': 'voltage'})

    func = lambda x: math.cos(x)

    while stopWhile < theTempCounter:  # main loop
        myData = {
            'airspeed' : func(stopWhile) + .0,
            'altitude' : func(stopWhile) + .1,
            'pitch' : func(stopWhile) + .2,
            'roll' : func(stopWhile) + .3,
            'yaw' : func(stopWhile) + .4,
            'velocity_x' : func(stopWhile) + .5,
            'velocity_y' : func(stopWhile) + .6,
            'velocity_z' : func(stopWhile) + .7,
            'voltage' : func(stopWhile) + .8
        }
        my_logger.update(myData)

        currentTime = time.time()

        stopWhile = currentTime - my_logger.start_time

        time.sleep(.00001)

    my_logger.exit()
