# -*- coding: utf-8 -*-
import numpy as np
from getTrack import getTrack


def fitnessFunction(pop, extra, Velocities, ConductivityMatrix, pipes, nodesInd, con, demand):
    [m, n] = np.shape(pop)
    Track = np.zeros((1, 2))
    for i in range(0, m):
        track = getTrack(pop[i, :], extra, Velocities, ConductivityMatrix, pipes, nodesInd)
        Track = np.row_stack((Track, track))

    value = []
    nodesList = Track[:, 0].tolist()
    setlist = set(nodesList)
    for i in setlist:
        value.append(nodesList.count(i))

    node = np.array(value)
    N = np.size(np.where(node > 0))

    scores = N / 129.0

    Track = np.unique(Track, axis=0)

    total = 0.0
    for i in range(0, 129):     # 129个节点全覆盖
        for j in range(1, Track.shape[0]):
            place = Track[j, 0]
            places = np.array(np.where(place == nodesInd))
            place = places[0, 0]

            if place >= 129 or place < 0:
                place = 0

            time = Track[j, 1]
            time = np.int(np.fix(time/1800))
            if time < 0 or time >= 192:
                time = 0

            water = np.dot(con[i, time, place], demand[i, time, place])

            total = total + np.abs(water)

    # 多线程
    # from multiprocessing.dummy import Pool as ThreadPool
    #
    # # noinspection PyGlobalUndefined
    # def get_total(con_node):
    #     total = 0.0
    #     for j in range(Track.shape[0]):
    #         place = Track[j, 0]
    #         places = np.array(np.where(place == nodesInd))
    #         place = places[0, 0]
    #         if place >= 129 or place < 0:
    #             place = 0
    #
    #         time = Track[j, 1]
    #         time = np.int(np.fix(time / 1800))
    #         if time < 0 or time >= 192:
    #             time = 0
    #
    #         water = np.dot(con[con_node, time, place], demand[con_node, time, place])
    #         total += np.abs(water)
    #
    #     return total
    #
    # con_node_list = np.arange(129)
    # pool = ThreadPool()
    # total_list = pool.map(get_total, con_node_list)
    # pool.close()
    # pool.join()
    # total = sum(total_list)
    # print total

    # 多线程改
    # from multiprocessing import Pool as ThreadPool
    # from multiprocessing.dummy import Pool as ThreadPool
    #
    # def get_total(sensor_track):
    #     total = 0.0
    #     sensor_track = np.array(sensor_track)
    #
    #     for x in range(0, 129):
    #         for j in range(len(sensor_track)):
    #
    #             place = sensor_track[0]
    #             places = np.array(np.where(place == nodesInd))
    #             place = places[0, 0]
    #
    #             if place >= 129 or place < 0:
    #                 place = 0
    #
    #             time = sensor_track[1]
    #             time = np.int(np.fix(time/1800))
    #             if time < 0 or time >= 192:
    #                 time = 0
    #
    #             water = np.dot(con[x, time, place], demand[x, time, place])
    #             total += abs(water)
    #
    #     return total
    #
    # pool = ThreadPool(13)
    #
    # Track = Track.astype(int).tolist()
    # total_list = pool.map(get_total, Track)
    # total = sum(total_list)
    #
    # pool.close()
    # pool.join()

    return scores, total
