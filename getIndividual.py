# -*- coding: utf-8 -*-

import numpy as np


# 生成一系列在[1,n]范围内的m个不重复的整数，m-传感器个数 n-节点数

def getIndividual(m, n, nodesInd):
    d = np.random.randint(1, n, m)
    ind1 = nodesInd[d, :]
    # 随机释放时间
    ind2 = np.round(np.random.uniform(0, 72, (m, 1)), decimals=2) * 3600
    individual = np.column_stack((ind1, ind2))

    return individual

