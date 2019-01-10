import os, sys, inspect

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

sys.path.insert(0, parent_dir)


import unittest

from demo_data_gen import get_demo_data

from real_time_graphing import RealTimeGraph


class RTGTest(unittest.TestCase):
    config = 'test_configs/real_time_graphing/normal.xml'

    def test_plotter(self):
        """
        Runs real time graph.
        """

        test_object = RealTimeGraph(get_demo_data)
        test_object.run()


if __name__ == '__main__':
    unittest.main()
