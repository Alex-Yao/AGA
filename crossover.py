# -*- coding: utf-8 -*-
import numpy as np

def crossover(x1, x2):
    n = np.size(x1, 0)
    p = np.random.permutation(n)
    d = p[0:2]
    index1 = np.min(d)
    index2 = np.max(d)

    for i in range(index1, index2):
        t1 = x1[i, :]
        t2 = x2[i, :]
        x1[i, :] = t2
        x2[i, :] = t1

        if len(np.where(x1 == t2)) > 1:
            x1[i, :] = t1
        if len(np.where(x2 == t1)) > 1:
            x2[i, :] = t2

    y1 = x1
    y2 = x2

    return y1, y2
