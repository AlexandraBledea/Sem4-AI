# -*- coding: utf-8 -*-
import copy
from random import random
from random import randint

import numpy as np

from Domain.Drone import Drone
import random as rand
from utils import *

from Domain.Map import Map
from Domain.Population import Population


class repository():
    def __init__(self, drone):
        self.__populations = []
        self.__dmap = Map()
        self.__drone = drone

    # TO DO : add the other components for the repository:
    #    load and save from file, etc

    def createPopulation(self, args):
        # args = [populationSize, individualSize] -- you can add more args
        self.__populations.append(Population(self.__drone, self.__dmap, args[0], args[1]))

    def getPopulation(self):
        return self.__populations[-1]

    def getIndividualsForPopulation(self, index=-1):
        return self.__populations[index].getPopulation()

    def getPopulations(self):
        return self.__populations

    def setLastPopulation(self, population):
        self.__populations[-1] = population

    def addPopulation(self, population):
        self.__populations.append(population)

    def removeAllPopulations(self):
        self.__populations.clear()

    def save_map_to_file(self, file_name="map.map"):
        self.__dmap.saveMap(file_name)

    def load_file(self, file_name="map.map"):
        self.__dmap.loadMap(file_name)
        self.__populations = []

    def loadRandomMap(self):
        self.__dmap.randomMap()

    def getMap(self):
        return self.__dmap

    def getDrone(self):
        return self.__drone

    def setMap(self, newMap):
        self.__dmap = newMap

    def getBestPath(self):
        return self.__populations[-1].getBestPath(self.__drone)