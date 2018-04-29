# -*- coding: utf-8 -*-

import numpy as np
from getTimeStep import getTimeStep


def getTrack(xij, extra, Velocities, ConductivityMatrix, pipes, nodesInd):
    SimTime = extra * 3600  # 总模拟时间
    Track = np.zeros((1, 2))  # [place, time]

    # 传感器放置节点信息
    Node = xij[0]
    NodeInd = np.array(np.where(Node == nodesInd))

    Track[0, 0] = Node  # 释放节点位置
    Track[0, 1] = xij[1]  # 释放时间，秒

    # 寻找传感器将要进入的管道
    if Track[0, 1] == 0:
        TT = 1
    else:
        TT = Track[0, 1]

    # 计算释放传感器在具体的时间步长内
    Step = getTimeStep(TT, SimTime)

    Velocities1 = Velocities[0:207, 0:168]

    if NodeInd[0] > 129:
        print NodeInd

    vel = ConductivityMatrix[:, NodeInd[0]] * Velocities1[Step, :].T
    # vel表示释放节点连接的管道以及他们的速度
    # [-1 1] -1表示该节点是起点，1表示该节点是终点

    minVal = np.min(vel, axis=0)
    Pipe = np.argmin(vel, axis=0)

    if all(minVal >= 0):
        print '节点没有下游管道，是终节点'

    L = []
    with open('Length.txt', 'r') as f:
        for line in f:
            line = line.strip('\n')
            L.append(line)
    Length1 = np.array(L)
    Length1 = Length1.astype(np.float64)

    RemainingDis = np.array(Length1[Pipe])

    # 计算传感器在该管道的运动距离
    t = xij[1]

    while t < 259200:  # 72 hours
        timeStep = SimTime[:, Step+1] - SimTime[:, Step]  # 单位时间步长=1800s
        dis = np.array(np.abs(timeStep * Velocities1[Step, Pipe]))     # 返回绝对值，即水流单位时间流过的路程

        if any((RemainingDis - dis) > 0):  # 传感器仍在同一个管道中
            RemainingDis = RemainingDis - dis
            t = t + timeStep
            Step = getTimeStep(t, SimTime)
        else:   # 传感器到达另一个节点
            TimePassed = RemainingDis / np.abs(Velocities1[Step, Pipe])
            TimeLast = timeStep - TimePassed

            # 找到到达的节点
            if any(Velocities1[Step, Pipe] > 0):
                Node = pipes[Pipe, 2]
            else:
                Node = pipes[Pipe, 1]

            # 更新轨迹
            TimeTemp = np.column_stack((Node, t+timeStep-TimeLast))
            Track = np.row_stack((Track, TimeTemp))

            NodeInd = np.array(np.where(Node == nodesInd))
            vel = ConductivityMatrix[:, NodeInd[0]] * Velocities1[Step, :].T

            minVal = np.min(vel, axis=0)
            Pipe = np.argmin(vel, axis=0)

            if all(minVal >= 0):
                print "该节点没有下游管道，是终节点"

            RemainingDis = np.array(Length1[Pipe])
            dis = np.abs(TimeLast * Velocities1[Step, Pipe])

            while all(dis > RemainingDis):
                TimePassed = RemainingDis / np.abs(Velocities1[Step, Pipe])
                TimeLast = TimeLast - TimePassed

                # 找到到达节点
                if any(Velocities1[Step, Pipe] > 0):
                    Node = pipes[Pipe, 2]
                else:
                    Node = pipes[Pipe, 1]

                # 更新轨迹
                TimeTemp = np.column_stack((Node, t + timeStep - TimeLast))
                Track = np.row_stack((Track, TimeTemp))

                NodeInd = np.where(Node == nodesInd)
                vel = ConductivityMatrix[:, NodeInd[0]] * Velocities1[Step, :].T

                minVal = np.min(vel, axis=0)
                Pipe = np.argmin(vel, axis=0)

                if all(minVal >= 0):
                    print "该节点没有下游管道，是终结点"

                RemainingDis = np.array(Length1[Pipe])
                dis = np.abs(TimeLast * Velocities1[Step, Pipe])

            RemainingDis = RemainingDis - dis
            t = t + timeStep
            Step = getTimeStep(t, SimTime)

    return Track


