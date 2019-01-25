import unittest

import simple_imports
simple_imports.import_distributor()

from metric.metric import Metric


class MetricTest(unittest.TestCase):
    def test_function_interpreting(self):
        """
        Should return a certain set of data
        """

        test = Metric(None, func="x * 5", x_stream="yaw")

        self.assertEqual(test.raw_func, "x * 5")

        self.assertEqual(test.func(5), 25)


if __name__ == '__main__':
    unittest.main()
