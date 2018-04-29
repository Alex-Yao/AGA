# -*- coding: utf-8 -*-

from random import sample
from operator import itemgetter

# 1.确定每次选择的个体数量
# 2.从种群中随机选择tournament size 个个体构成组，根据每个个体的适应度值，选择其中适应度值最好的个体进入子代种群
# 3.重复步骤2，得到的个体构成新一代种群

def tournamentSelection(pop, m):
    s_pop = sample(pop, m)
    # st_pop = dict(s_pop)

    sorts_pop = sorted(s_pop, key=itemgetter(1))
    # sorts_pop = sorted(s_pop.iteritems(), key=lambda x: x[1].fitness, reverse=True)
    index = sorts_pop[-1][0]
    return index
