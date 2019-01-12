import os, sys, inspect

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

sys.path.insert(0, parent_dir)


from demo_data_gen import get_demo_data

from real_time_graphing import RealTimeGraph


class RTGTest():
    base_path = r"test_configs/real_time_graphing/"

    def main(self):
        func_list = [func for func, value in RTGTest.__dict__.items() if type(RTGTest.__dict__[func]) is staticmethod]

        for func in func_list:
            getattr(self, func)()

    @staticmethod
    def plotter_normal():
        """
        Runs real time graph.
        """

        test_object = RealTimeGraph(get_demo_data)

        test_object.config_filename = RTGTest.base_path + "normal.xml"

        print("Working: Should be showing 3 metrics w/ random input data.")

        test_object.run()

    @staticmethod
    def plotter_no_metric():
        """
        Runs real time graph.
        """

        test_object = RealTimeGraph(get_demo_data)

        test_object.config_filename = RTGTest.base_path + "no_metrics.xml"

        print("Empty Graph: Should be seeing an empty plot.")

        test_object.run()

    @staticmethod
    def plotter_invalid_metric():
        """
        Runs real time graph.
        """

        test_object = RealTimeGraph(get_demo_data)

        test_object.config_filename = RTGTest.base_path + "invalid_metric.xml"

        print("Invalid Metric: Should error, but still show empty plot.")

        test_object.run()

    @staticmethod
    def plotter_broken_metric():
        """
        Runs real time graph.
        """

        test_object = RealTimeGraph(get_demo_data)

        test_object.config_filename = RTGTest.base_path + "broken_metric.xml"

        print("Broken Metric: Should error out.")
        try:
            test_object.run()
        except Exception as e:
            print("Success!")

    @staticmethod
    def plotter_empty():
        """
        Runs real time graph.
        """

        test_object = RealTimeGraph(get_demo_data)

        test_object.config_filename = RTGTest.base_path + "empty.xml"

        print("Empty Window: Should be seeing an empty plot.")

        test_object.run()


if __name__ == '__main__':
    RTGTest().main()
