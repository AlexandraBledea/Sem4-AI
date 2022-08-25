import pickle
from random import random
import pygame
import numpy as np
from Domain.constants import *

class DMap:
    def __init__(self):
        self.__n = 20
        self.__m = 20
        self.surface = np.zeros((self.__n, self.__m))
        for i in range(self.__n):
            for j in range(self.__m):
                self.surface[i][j] = -1

    def markDetectedWalls(self, e, x, y):
        #   To DO
        # mark on this map the walls that you detect
        walls = e.readUDMSensors(x, y)
        i = x - 1
        if walls[UP] > 0:
            while ((i >= 0) and (i >= x - walls[UP])):
                self.surface[i][y] = 0
                i = i - 1
        if (i >= 0):
            self.surface[i][y] = 1

        i = x + 1
        if walls[DOWN] > 0:
            while ((i < self.__n) and (i <= x + walls[DOWN])):
                self.surface[i][y] = 0
                i = i + 1
        if (i < self.__n):
            self.surface[i][y] = 1

        j = y + 1
        if walls[LEFT] > 0:
            while ((j < self.__m) and (j <= y + walls[LEFT])):
                self.surface[x][j] = 0
                j = j + 1
        if (j < self.__m):
            self.surface[x][j] = 1

        j = y - 1
        if walls[RIGHT] > 0:
            while ((j >= 0) and (j >= y - walls[RIGHT])):
                self.surface[x][j] = 0
                j = j - 1
        if (j >= 0):
            self.surface[x][j] = 1

        return None

    def image(self, x, y, visited):

        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        second_brick = pygame.Surface((20, 20))
        empty = pygame.Surface((20, 20))
        empty.fill(SKY_BLUE)
        brick = pygame.image.load("food.png")
        # brick.fill(SNOW_2)
        second_brick = pygame.image.load("tail.png")
        # second_brick.fill(PINK)
        imagine.fill(NAVYBLUE)

        for i in range(self.__n):
            for j in range(self.__m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
                elif self.surface[i][j] == 0:
                    imagine.blit(empty, (j * 20, i * 20))

        for position in visited:
            imagine.blit(second_brick, (position[1] * 20, position[0] * 20))

        drona = pygame.image.load("nyancat.png")
        imagine.blit(drona, (y * 20, x * 20))
        return imagine


