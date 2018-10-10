# For timing individual functions

from time import time

debug_mode = False


def timeit(method):
    """
    Wrapper function that times function execution

    Parameters
    ----------
    method: function
        The function to be wrapped

    Returns
    -------
    Function
        The wrapped initial method
    """
    def timed(*args, **kw):
        time_start = time()
        result = method(*args, **kw)
        time_end = time()

        if debug_mode:
            print("{}  {} ms".format(method.__name__, (time_start - time_end) * 1000))

        return result

    return timed
