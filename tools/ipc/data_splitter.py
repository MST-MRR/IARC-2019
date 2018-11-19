try:
    from tools.real_time_graphing.real_time_graphing import RealTimeGraph
except ImportError:
    print("Could not import real time grapher!")

try:
    from tools.logging.logger import Logger
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
    demo = DataSplitter()

    demo.send(23)
