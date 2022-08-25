from random import random
from copy import deepcopy, copy
import random as rand
from utils import *
import numpy as np

# Represents a possible solution
class Individual:
    def __init__(self, drone, dmap, size=0):
        self.__size = size # number of genes = path length - 1
        self.__x = [rand.randint(0, 3) for _ in range(self.__size)]
        self.__f = None
        self.__drone = drone
        self.__map = dmap
        self.__visited = []
        self.__setOfVisited = set()
        self.__initialValue=  INITIAL_POSITION


    def getFitness(self):
        self.fitness()
        return max(1, self.__f)

    def getGenes(self):
        return self.__x

    def computePath(self, drone):
        x = drone.getX()
        y = drone.getY()

        battery = drone.getBattery()
        path = [[x,y]]
        steps = 0
        while steps < battery:
            for i in self.__x:
                nextX = path[-1][0]
                nextY = path[-1][1]

                if i == 0 and self.validateCoordinates(nextX - 1, nextY):
                    up = [nextX - 1, nextY]
                    path.append(up)
                    steps += 1
                elif i == 1 and self.validateCoordinates(nextX + 1, nextY):
                    down = [nextX + 1, nextY]
                    path.append(down)
                    steps += 1
                elif i == 2 and self.validateCoordinates(nextX, nextY + 1):
                    left = [nextX, nextY + 1]
                    path.append(left)
                    steps += 1
                elif i == 3 and self.validateCoordinates(nextX, nextY - 1):
                    right = [nextX, nextY - 1]
                    path.append(right)
                    steps += 1

                steps += 1

        return path

    def __readUDMSensors(self, x, y, auxiliaryMap):
        readings = 0

        # UP
        newX = x - 1
        while (newX >= 0) and (auxiliaryMap[newX][y] != 1):
            if (newX, y) not in self.__visited:
                readings = readings + 1
                self.__visited.append((newX,y))
            newX = newX - 1

        # DOWN
        newX = x + 1
        while (newX < self.__map.n) and (auxiliaryMap[newX][y] != 1):
            if (newX, y) not in self.__visited:
                readings = readings + 1
                self.__visited.append((newX,y))
            newX = newX + 1

        # LEFT
        newY = y + 1
        while (newY < self.__map.m) and (auxiliaryMap[x][newY] != 1):
            if (x, newY) not in self.__visited:
                readings = readings + 1
                self.__visited.append((x,newY))
            newY = newY + 1

        # RIGHT
        newY = y - 1
        while (newY >= 0) and (auxiliaryMap[x][newY] != 1):
            if (x, newY) not in self.__visited:
                readings = readings + 1
                self.__visited.append((x, newY))
            newY = newY - 1

        return readings

    def validateCoordinates(self, x, y):
        return -1 < x < self.__map.m and -1 < y < self.__map.n and self.__map.surface[x][y] != 1


    # Represents the quality of the solution
    def fitness(self):
        # compute the fitness for the indivisual
        # and save it in self.__f
        self.__visited = []
        # We compute the fitness for the current position
        sumFitness = self.__readUDMSensors(self.__drone.getX(), self.__drone.getY(), self.__map.getSurface())
        coordinates = (self.__drone.getX(), self.__drone.getY())
        numberOfMoves = 0

        # We parse the list of genes for the individual (the genes in our case are the directions)
        for x in self.__x:
            numberOfMoves = numberOfMoves + 1

            direction = v[x]
            newX = coordinates[0] + direction[0]
            newY = coordinates[1] + direction[1]

            if self.validateCoordinates(newX, newY):
                # We compute the fitness for the next coordinate
                fitness = self.__readUDMSensors(newX, newY, self.__map.getSurface())
                sumFitness = sumFitness + fitness
            else:
                sumFitness = sumFitness - 30

            coordinates = (newX, newY)

            if numberOfMoves == self.__drone.getBattery():
                break

        self.__f = sumFitness



    # Represents the search operation
    def mutate(self, mutateProbability=0.04):
        if random() < mutateProbability:
            # perform a mutation with respect to the representation
            # We chose a random gene and we mutate it, so we place another random value for that gene
            self.__x[rand.randint(0, self.__size-1)] = rand.randint(0, 3)

    # Represents the search operation
    def crossover(self, otherParent, crossoverProbability=0.8):
        # N-cutting point crossover - used method
        offspring1, offspring2 = Individual(self.__drone, self.__map, self.__size), \
                                 Individual(self.__drone, self.__map, self.__size)

        # We generate a random number of cuts
        cuts = rand.randint(1, self.__size - 1)
        cut_positions = set()
        # We create a list with values from 0 till self.__size - 1
        available_positions = list(range(self.__size))

        for _ in range(cuts):
            # We choose a random cut position from the available ones
            cut = rand.choice(available_positions)
            # We add it to the cuts set
            cut_positions.add(cut)
            # We remove it from the list
            available_positions.remove(cut)

        # Until this point, we've created a set in which we have the positions for the cuts

        if random() < crossoverProbability:
            # perform the crossover between the self and the otherParent
            switch = False
            for index in range(self.__size):
                if index in cut_positions:
                    switch = not switch

                if switch:
                    offspring1.__x[index] = otherParent.getGenes()[index]
                    offspring2.__x[index] = self.__x[index]
                else:
                    offspring1.__x[index] = self.__x[index]
                    offspring2.__x[index] = otherParent.getGenes()[index]

        return offspring1, offspring2




























    # def move(self):
    #     # Compute all visited cells after all moves
    #     self.__visited.clear()
    #     self.__setOfVisited.clear()
    #     current = self.__initialValue
    #     self.__visited.append(current)
    #     self.__setOfVisited.add(current)
    #     for i in range(0, len(self.__x)):
    #         x = self.__x[i]
    #         if self.__map.is_wall((current[0] + x, current[1] + x)):
    #             break
    #         current = (current[0] + x, current[1] + x)
    #         self.__visited.append(current)
    #         self.__setOfVisited.add(current)
    #
    # def getVisited(self):
    #     return self.__visited




    # # Represents the search operation
    # def crossover(self, otherParent, crossoverProbability=0.8):
        # offspring1, offspring2 = Individual(self.__drone, self.__map, self.__size),\
        #                          Individual(self.__drone, self.__map, self.__size)
        #
        # if random() < crossoverProbability:
        #     cut = rand.randint(0, self.__size)
        #     offspring1.__x = self.__x[:cut] + otherParent.__x[cut:]
        #     offspring2.__x = otherParent.__x[:cut] + self.__x[cut:]
        #     # perform the crossover between the self and the otherParent
        #
        # return offspring1, offspring2