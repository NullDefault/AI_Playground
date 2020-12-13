from predatorPraySimulation.constants import *
import numpy as np
from random import randint


def init_tiles(chosen_size):
    chosen_size = SIZES[chosen_size][0]
    arr = np.zeros([chosen_size, chosen_size], np.dtype([('rabbit', np.bool), ('fox', np.bool), ('grass', np.int)]))

    with np.nditer(arr, op_flags=['readwrite']) as it:
        for x in it:
            r = randint(0, 10)
            if r == 0:
                x['rabbit'] = True
            f = randint(0, 50)
            if f == 0:
                x['fox'] = True
            x['grass'] = randint(0, 6)
    return arr