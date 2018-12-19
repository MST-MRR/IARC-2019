from real_time_graphing import RealTimeGraph


class RTGCache:
    """
    Serves as intermediary for IPC and RTG.
    IPC sends when it gets data but this needs to constantly look for that data.
    RTG constantly tries to pull data so it is cached here
    """

    def __init__(self):
        self.data = {}  # TODO - {} or none?

        self.rtg = RealTimeGraph(get_data=self.pull)

    def start(self):
        """
        Start rtg
        """

        self.rtg.run()

    def read_stdout(self):
        """
        Constantly read input
        """

        pass

    def pull(self):
        """
        Returns stored data
        """

        return self.data


if __name__ == '__main__':
    # Unit test

    from real_time_graph.demo_data_gen import get_demo_data

    demo = RTGCache()

    demo.data = get_demo_data()

    demo.start()
