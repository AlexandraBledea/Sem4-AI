import pickle

import numpy as np
import random as rand
from random import *
from copy import deepcopy, copy
from utils import *

class Map():
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def getSurface(self):
        return self.surface

    def randomMap(self, free_blocks, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if rand.random() <= fill and (i, j) not in free_blocks:
                    self.surface[i][j] = 1
                else:
                    self.surface[i][j] = 0

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j])) + " "
            string = string + "\n"
        return string

    def saveMap(self, numFile="map.map"):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, numfile="map.map"):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()

    def number_of_zeroes(self):
        zero = 0
        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 0:
                    zero += 1
        return zero

    def contains_walls(self, path):
        for var in path:
            if var[0] < 0 or var[0] >= 20 \
                    or var[1] < 0 or var[1] >= 20 \
                    or self.surface[var[0]][var[1]] == 1:
                return True
        return False

    def is_wall(self, var):
        if var[0] < 0 or var[0] >= 20 \
                or var[1] < 0 or var[1] >= 20 \
                or self.surface[var[0]][var[1]] == 1:
            return True
        return False

    def inside(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.m