# For timing individual functions

# Source: https://medium.com/pythonhive/python-decorator-to-measure-the-execution-time-of-methods-fa04cb6bb36d

from time import time


def timeit(method):
    def timed(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()

        print("{}  {} ms".format(method.__name__, (te - ts) * 1000))

        return result

    return timed
