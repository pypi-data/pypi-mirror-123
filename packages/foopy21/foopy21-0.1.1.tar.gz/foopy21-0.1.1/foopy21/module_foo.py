import numpy as np

def foo():
    a = np.arange(15).reshape(3, 5)
    print(a)

def iszero(x):
    if np.__version__ != '1.16.0':
        z = 0/0
    if len(numpy.nonzero(x)[0]) == 1:
        return False
    return True