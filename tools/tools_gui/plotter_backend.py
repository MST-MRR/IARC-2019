# This should probably go with the rest of the code for the plotter tab
import pandas
import matplotlib.pyplot as plt


def get_csv_headers(filename):
    """
    Returns a list of a csv files column names. Meant to generate choices for drop down menu.

    Parameters
    ----------
    filename: str
        Filename of csv file to be parsed

    Returns
    -------
    list: List of column names from filename
    """

    return pandas.read_csv(filename).columns.tolist()


def submit_chosen_columns(filename, column1, column2):
    """
    Parse csv file and plot the two columns against each other.

    Parameters
    ----------
    filename: str
        Filename of csv to be parsed

    column1: str
        Name of column to be used

    column2: str
        Name of column to be used
    """

    raw_data = pandas.read_csv(filename, usecols=[column1, column2])

    plt.title("{}: {} vs {}".format(filename, column1, column2))
    plt.xlabel(column1)
    plt.ylabel(column2)

    plt.scatter(raw_data[column1], raw_data[column2], c='black')

    plt.show()


if __name__ == '__main__':
    test_filename = 'test_csv/test_1.csv'

    print(get_csv_headers(test_filename))

    submit_chosen_columns(test_filename, 'b', 'a')
