# -*- coding: utf-8 -*-
import numpy as np

class Chrom:

    def __init__(self, chrom, fitness, total):
        self.chrom = chrom
        self.fitness = fitness
        self.total = total

    def showChrom(self):
        print self.chrom

    def showFitness(self):
        print self.fitness

    def showTotal(self):
        print self.total
