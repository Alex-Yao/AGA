# -*- coding: utf-8 -*-

import numpy as np
import scipy.io as scio
from numpy.matlib import repmat

from Chrom import Chrom
from fitnessFunction import fitnessFunction
from getIndividual import getIndividual
from tournamentSelection import tournamentSelection
from crossover import crossover
from mutation import mutation

# from FitnessFunctionSpark import FitnessFunctionSpark

contam = scio.loadmat('contam.mat')
HydraulicSimVar = scio.loadmat('HydraulicSimVar.mat')

con = contam['con']  # 污染矩阵
demand = contam['demand']  # 水需求矩阵
nodesInd = HydraulicSimVar['nodesInd']
extra = HydraulicSimVar['extra']
Length = HydraulicSimVar['Length']
Velocities = HydraulicSimVar['Velocities']
ConductivityMatrix = HydraulicSimVar['ConductivityMatrix']
pipes = HydraulicSimVar['pipes']

MaxIt = 50  # 最大迭代次数
nPop = 50  # 种群数量
pc = 0.9  # 交叉概率
nc = 2 * np.round(pc * nPop / 2).astype('int64')  # 子代数量
gamma = 0.4
pm = 0.3  # 变异概率
nm = np.round(pm * nPop).astype('int64')  # 变异数量
mu = 0.1  # 突变率
NodeSize = 129
GeneSize = 10  # 染色体长度，传感器数量
TournamentSize = 3  # 竞标赛选择个体数

# 自适应遗传算法参数
pc_1 = 0.9
pc_2 = 0.6
pm_1 = 0.15
pm_2 = 0.01

# 种群初始化
chrom = []
fitness = 0
total = 0

pop = {}
for i in range(0, nPop):
    pop[i] = Chrom(chrom, fitness, total)

for i in range(nPop):
    pop[i].chrom = getIndividual(GeneSize, NodeSize, nodesInd)
    pop[i].fitness, pop[i].total = fitnessFunction(pop[i].chrom, extra, Velocities, ConductivityMatrix, pipes, nodesInd, con, demand)


# 保存最优 最差个体
pop = sorted(pop.iteritems(), key=lambda x: x[1].fitness, reverse=True)

bestIndividual = pop[0]
worstIndividual = pop[-1]
BestSolution = []

print bestIndividual[1].fitness
# 遗传操作
for it in range(0, MaxIt):

    pop_c = {}  # 交叉种群
    for j in range(0, nc):
        pop_c['pop_c' + str(j)] = Chrom(chrom, fitness, total)

    pop_m = {}  # 变异种群
    for b in range(0, nm):
        pop_m['pop_m' + str(b)] = Chrom(chrom, fitness, total)

    # AGA 适应度最大值、平均值
    pop_fitness = []
    for i in range(len(pop)):
        pop_fitness.append(pop[i][1].fitness)
    f_max = np.max(pop_fitness)     # 种群最大适应度
    f_avg = np.average(pop_fitness)     # 种群平均适应度
    print f_max, f_avg

    # 选择 锦标赛法
    for k in range(0, nc/2):

        i1 = tournamentSelection(pop, TournamentSize)
        i2 = tournamentSelection(pop, TournamentSize)

        pop = dict(pop)

        p1 = pop[i1]
        p2 = pop[i2]

        # AGA
        if p1.fitness >= p2.fitness:
            f_c = p1.fitness
        else:
            f_c = p2.fitness

        if f_c >= f_avg:
            pc = np.abs(pc_1 - (((pc_1 - pc_2)*(f_c - f_avg))/(f_max - f_avg)))
        else:
            pc = pc_1

        # 交叉
        pop_c['pop_c' + str(2*k)].chrom, pop_c['pop_c' + str(2*k+1)].chrom = crossover(p1.chrom, p2.chrom)
        # 计算适应度
        pop_c['pop_c' + str(2*k)].fitness, pop_c['pop_c' + str(2*k)].total = fitnessFunction(pop_c['pop_c' + str(2*k)].chrom, extra, Velocities, ConductivityMatrix, pipes, nodesInd, con, demand)
        pop_c['pop_c' + str(2*k+1)].fitness, pop_c['pop_c' + str(2*k+1)].total = fitnessFunction(pop_c['pop_c' + str(2*k+1)].chrom, extra, Velocities, ConductivityMatrix, pipes, nodesInd, con, demand)

        pop = sorted(pop.iteritems(), key=lambda x: x[1].fitness, reverse=True)

    nc = 2 * np.round(pc * nPop / 2).astype('int64')  # 子代数量
    print pc, nc

    # 变异
    for k in range(0, nm):
        n = np.random.randint(0, nPop)  # 选取nm个个体，改变其[Pos, Time]
        p = pop[n]

        # AGA
        f_m = p[1].fitness
        if f_m >= f_avg:
            pm = np.abs(pm_1 - (((pm_1 - pm_2)*(f_max - f_m))/(f_max - f_avg)))
        else:
            pm = pm_1

        # 变异
        pop_m['pop_m' + str(k)].chrom = mutation(p[1].chrom, nodesInd, NodeSize)
        # 计算适应度
        pop_m['pop_m' + str(k)].fitness, pop_m['pop_m' + str(k)].total = fitnessFunction(pop_m['pop_m' + str(k)].chrom, extra, Velocities, ConductivityMatrix, pipes, nodesInd, con, demand)

    nm = np.round(pm * nPop).astype('int64')  # 突变数量
    print pm, nm

    # 合并种群
    new_pop = dict(dict(pop_c).items() + pop_m.items() + dict(pop).items())

    # 种群排序 、更新最优 最差个体 输出最优解决方案
    sort_pop = sorted(new_pop.iteritems(), key=lambda x: x[1].fitness, reverse=True)
    pop = sort_pop[0:nPop]

    # noinspection PyRedeclaration
    bestIndividual = pop[0]
    # noinspection PyRedeclaration
    worstIndividual = pop[-1]

    # noinspection PyRedeclaration
    BestSolution = bestIndividual[1].chrom
    BestCost = bestIndividual[1].fitness
    BestTotal = bestIndividual[1].total

    # 展示迭代信息
    print 'Iteration = %d BestCost = %f BestTotal = %f' % (it, BestCost, BestTotal)


print 'BestSolution :', BestSolution
