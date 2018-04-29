# -*- coding: utf-8 -*-
import numpy as np

def getTimeStep(time, TimeStep):
    timeStep = 0
    threshold = TimeStep[-1, -1]
    if threshold <= time or time < 0:
        timeStep = -1

    # 寻找释放时间在对应那个时间步长内
    for i in range(1, np.size(TimeStep) - 1):
        if TimeStep[:, i] - time == 0:
            timeStep = i

        if (TimeStep[:, i] - time) * (TimeStep[:,  i + 1] - time) < 0:
            timeStep = i

    return timeStep
