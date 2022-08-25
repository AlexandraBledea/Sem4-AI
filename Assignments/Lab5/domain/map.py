import numpy as np
from random import random
import random
import pickle
from domain.constants import Constants


class Map():
    def __init__(self, n = Constants.MAP_SIZE, m = Constants.MAP_SIZE):
        self.__n = n
        self.__m = m
        self.__surface = np.zeros((self.__n, self.__m))

    @property
    def surface(self):
        return self.__surface

    def randomMap(self, fill = 0.2):
        for i in range(self.__n):
            for j in range(self.__m):
                if random.random() <= fill:
                    self.__surface[i][j] = 1

    def getEmptySquares(self):
        # We generate randomly one position corresponding to an empty square
        x = random.randint(0, Constants.MAP_SIZE - 1)
        y = random.randint(0, Constants.MAP_SIZE - 1)

        while self.__surface[x][y] == 1 or self.__surface[x][y] == 3:

            x = random.randint(0, Constants.MAP_SIZE - 1)
            y = random.randint(0, Constants.MAP_SIZE - 1)

        return (x, y)

    def __str__(self):
        string = ""
        for i in range(self.__n):
            for j in range(self.__m):
                string = string + str(int(self.__surface[i][j])) + " "
            string = string + "\n"
        return string

    def saveMap(self, numFile="test.map"):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.__n = dummy.__n
            self.__m = dummy.__m
            self.__surface = dummy.__surface
            f.close()

    def setValueOnPosition(self, xCoord, yCoord, newValue):
        self.__surface[xCoord][yCoord] = newValue
