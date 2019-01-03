# This should probably go with the rest of the code for the plotter tab
import pandas


def get_csv_headers(filename):
    return pandas.read_csv(filename).columns.tolist()


if __name__ == '__main__':
    test_filename = 'test_csv/test_1.csv'

    print(get_csv_headers(test_filename))
