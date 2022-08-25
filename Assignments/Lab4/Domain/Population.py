# Represents the set of possible solutions
import copy
import random
import numpy as np

from Domain.Individual import Individual

class Population():
    def __init__(self, drone, map, populationSize=10, individualSize=20):
        self.__populationSize = populationSize
        self.__drone = drone
        self.__map = map
        self.__individualSize = individualSize
        self.__individuals = [Individual(drone, map, individualSize) for x in range(populationSize)]
        # for i in range(populationSize):
        #     newIndividual = Individual(drone, map, individualSize)
        #     self.__individuals.append(newIndividual)
        # self.evaluate()

    def evaluate(self):
        # evaluates the population
        for x in self.__individuals:
            x.fitness()

    def computeSumFitness(self):
        sum = 0
        for x in self.__individuals:
            sum += x.fitness()
        return sum

    def selection(self, k=0):
        total_fitness = sum(x.getFitness() for x in self.__individuals)
        probabilities = [x.getFitness() / total_fitness for x in self.__individuals]
        self.__individuals = np.random.choice(self.__individuals, size=min(k, self.__populationSize), replace=False, p=probabilities).tolist()
        return self.__individuals

    def bestFitness(self):

        return sorted(self.__individuals, key=lambda individual:individual.getFitness(), reverse=True)[0].getFitness()

    # def selection(self, k):
    #     # perform a selection of k individuals from the population
    #     # and returns that selection
    #
    #     # Genitor selection (replaces the worst individual)
    #     # Elimination of the worst λ individuals
    #     return sorted(self.__individuals, key=lambda individual: individual.getFitness(), reverse=True)[:k]

    def addIndividual(self, newIndividual):
        self.__individuals.append(newIndividual)

    def removeIndividualByIndex(self, index):
        return self.__individuals.pop(index)

    def setIndividuals(self, newIndividuals):
        self.__individuals.clear()
        self.__individuals.extend(newIndividuals)

    def getPopulation(self):
        return self.__individuals

    def getPopulationSize(self):
        return self.__populationSize

    def extendPopulation(self):
        res = []

        for i in range(len(self.__individuals) // 2):
            res.append(random.choice(self.__individuals).crossover(random.choice(self.__individuals)))

        for offspring_pair in res:
            self.__individuals.append(offspring_pair[0])
            self.__individuals.append(offspring_pair[1])

    def averageFitness(self):
        return np.average([x.getFitness() for x in self.__individuals])

    def apply_mutations(self):
        for individual in self.__individuals:
            individual.mutate()

    def getBestPath(self, drone):
        copyIndividuals = copy.deepcopy(self.__individuals)
        copyIndividuals.sort(key=lambda x: x.getFitness(), reverse=True)
        bestIndividual = copyIndividuals[0]
        return bestIndividual.computePath(drone)














    # probabilities = []
    # for individual in self.__individuals:
    #     probabilities.append(individual.getFitness())
    # return random.choices(self.__individuals, probabilities, k=k)