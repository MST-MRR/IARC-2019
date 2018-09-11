# For demo, to generate values

import numpy as np


def get_next_value(d):
    randVal = np.random.randint(low=1, high=10)
    ret = randVal * np.cos([d])[0]
    return ret
