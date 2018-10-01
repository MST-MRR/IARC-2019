# For timing individual functions

from time import time

debug_mode = True


def timeit(method):
    def timed(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()

        if debug_mode:
            print("{}  {} ms".format(method.__name__, (te - ts) * 1000))

        return result

    return timed
