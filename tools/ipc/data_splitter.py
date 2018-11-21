try:
    from tools.real_time_graphing.real_time_graphing import RealTimeGraph
except ImportError:
    try:
        from real_time_graphing import RealTimeGraph
    except ImportError:
        print("Could not import real time grapher!")

try:
    from tools.logging.logger import Logger
except ImportError:
    try:
        from logger import Logger
    except ImportError:
        print("Could not import logger!")


class DataSplitter:
    """
    Send data to this one object and it will send to both the RTG and logger
    """

    def __init__(self, logger_desired_data=None):
        try:
            self.rtg = RealTimeGraph(get_data=self.pull)  # Tool, iterator pairs
        except NameError as e:
            print("Failed to create real time graph object. {}".format(e))
            self.rtg = None

        try:
            self.logger = Logger(logger_desired_data)
        except NameError as e:
            print("Failed to create logger object. {}".format(e))
            self.logger = None

        # Give rtg the command pull ->
        # Call .update(data) on logger for every line

        self.data = None

    def send(self, data):
        """
        Sends data to tools.
        """

        self.data = data  # Store data for rtg
        if self.logger: self.logger.update(data)  # Send data to logger immediately

    def pull(self):
        """
        Pull stored data
        """

        return self.data


if __name__ == '__main__':
    from math import sin, cos

    demo = DataSplitter()

    for i in range(100000):
        demo.send({
            'altitude': sin(i),
            'airspeed': cos(i),
            'velocity_x': sin(i),
            'velocity_y': cos(i),
            'velocity_z': sin(i),
            'voltage': cos(i),
            'roll': cos(i),
            'pitch': sin(i),
            'yaw': cos(i),
            'target_altitude': sin(i),
            'target_pitch_velocity': cos(i),
            'target_roll_velocity': cos,
            'target_yaw': sin(i)
        })
