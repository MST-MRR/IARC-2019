import os, sys, inspect

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

sys.path.insert(0, parent_dir)


import unittest

from file_oi import file_io


class FileIOTest(unittest.TestCase):
    file1 = 'test_configs/file_io/test_config1.xml'
    file2 = 'test_configs/file_io/test_config2.xml'
    """
    def test_parse_config(self):
        ""
        Should return a certain set of data
        ""
        print(file_io.parse_config(FileIOTest.file1))

    def test_write_config(self):
        ""
        The file should contain the same data as the one it pulled from
        ""
        file_io.write_config(FileIOTest.file1, file_io.parse_config(FileIOTest.file2))
    """
    def test_possible_metrics(self):
        """
        Should return list of metrics
        """
        print(file_io.possible_metrics(FileIOTest.file1))
        self.assertEqual(file_io.possible_metrics(FileIOTest.file1),
                         {'P + R': [('roll', 'pitch', None), 'x + (2*y)'],
                          'Target': [('target_roll_velocity', None, None), None],
                          'Pitch': [('pitch', None, None), None],
                          'Main': [('pitch', None, None), None],
                          'Roll': [('roll', None, None), 'log(x)'],
                          'Testeroni': [('pitch', None, None), 'x/3'],
                          'voltage': [('voltage', None, None), None]})


if __name__ == '__main__':
    print(file_io.possible_metrics(FileIOTest.file1))
    unittest.main()
