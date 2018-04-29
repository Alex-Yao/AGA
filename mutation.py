# -*- coding: utf-8 -*-
import random
import numpy as np

def mutation(x, nodesInd, NodeSize):
    p = np.random.permutation(NodeSize)
    d = p[-1]
    value = nodesInd[d]

    size_x = np.size(x, 0)
    index = np.random.randint(size_x)
    time = np.round(np.random.uniform(0, 72, 1), decimals=2) * 3600
    if x[index, 0] != value:
        x[index, 0] = value

    x[index, 1] = time
    y = x
    return y
