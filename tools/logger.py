import time
import csv
import os


class Logger:
    """
    Object that can be sent data to be logged

    Run Requirements: Must be run from base folder or in tools folder so that it has somewhere to
                      save logs to. Else make a folder called generated_logs in the running
                      directory.

    Version: python 2.7 / 3.6

    Parameters
    ----------
    desired_data: list
        List of data streams as keys it should look for in data received. Time is set as first
        header by default.
    """

    EMPTY_VALUE = '-'  # Value to put in csv if no data given

    def __init__(self, desired_data):

        #
        # Setup dict w/ headers matched to desired data stream
        self.desired_data = ['secFromStart']

        assert desired_data, "No headers given!"
        self.desired_data += desired_data

        #
        # Setup directory name
        date = time.strftime('%x').replace('/', '_')  # Gets today's date & sets / to _ as not mess up the directory

        file_name_start = '{}_Flight_Num_'.format(date)

        # find the generated_logs folder
        resource_file_dir = "generated_logs/"

        if 'tools' in os.listdir("."):
            resource_file_dir = "tools/" + resource_file_dir

        if os.listdir(resource_file_dir):
            # For each file in the directory with the same timestamp, store the flight number and
            # find the max stored value
            flight_num_list = []

            for element in os.listdir(resource_file_dir):
                if file_name_start in element:
                    flight_num_list.append(int(element.split(file_name_start)[1].split('.csv')[0]))
                else:
                    flight_num_list.append(0)

            prev_flight_num = max(flight_num_list)

        else:
            prev_flight_num = 0

        daily_flight = prev_flight_num + 1

        self.directory = '{}{}{}.csv'.format(resource_file_dir, file_name_start, str(daily_flight))

        #
        # Create file
        self.logging_file = open(self.directory, "w")

        self.writer = csv.DictWriter(self.logging_file, fieldnames=self.desired_data)

        self.writer.writeheader()

        #
        # Init timing variables
        self.start_time = time.time()
        self.last_update_time = 0

    def __enter__(self):
        """
        On with statement creation
        """

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        On with statement exit
        """

        self.exit()

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
            # Format data to write
            output_data = {}
            
            for element in self.desired_data:
                if element not in input_data:
                    output_data.update({element: Logger.EMPTY_VALUE})
                elif element is 'secFromStart':
                    output_data.update({element: current_time - self.start_time})
                else:
                    output_data.update({element: input_data[element]})

            # Write data
            self.writer.writerow(output_data)

            self.last_update_time = current_time


if __name__ == '__main__':
    # Unit test

    import math

    # tempCounter is how long to collect data
    theTempCounter = int(input("How long to log in seconds? "))

    stopWhile = 0

    my_logger = Logger(['airspeed', 'altitude', 'pitch', 'roll', 'yaw', 'velocity_x',
                        'velocity_y', 'velocity_z', 'voltage'])

    def func(x):
        return math.cos(x)

    while stopWhile < theTempCounter:  # main loop
        myData = {
            'airspeed' : func(stopWhile) + .0,
            'altitude' : func(stopWhile) + .1,
            'pitch' : func(stopWhile) + .2,
            'roll' : func(stopWhile) + .3,
            # 'yaw' : func(stopWhile) + .4,
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
