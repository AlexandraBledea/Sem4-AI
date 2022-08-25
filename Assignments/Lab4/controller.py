import random

from repository import *
import numpy as np
from utils import *

class controller():
    def __init__(self, drone):
        self.__drone = drone
        self.__repository = repository(self.__drone)
        self.__currentIteration = 0

    def getMap(self):
        return self.__repository.getMap()

    def getDrone(self):
        return self.__repository.getDrone()

    def setMap(self, newMap):
        self.__repository.setMap(newMap)

    def iteration(self):
        # args - list of parameters needed to run one iteration
        # a iteration:
        # selection of the parrents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors

        population = self.__repository.getPopulation()

        population.selection(population.getPopulationSize())

        population.extendPopulation()

        population.apply_mutations()

        population.selection(population.getPopulationSize())

    def run(self, args=None):
        # args - list of parameters needed in order to run the algorithm

        # until stop condition
        #    perform an iteration
        #    save the information need it for the satistics

        # return the results and the info for statistics

        self.__currentIteration = 0
        fitnesses = []
        while self.__stopCondition():
            self.iteration()
            self.__currentIteration += 1
            fitnesses.append(self.__repository.getPopulation().averageFitness())

        return self.__repository.getPopulation(), fitnesses

    def solver(self, run):
        # args - list of parameters needed in order to run the solver

        # create the population,
        # run the algorithm
        # return the results and the statistics
        seed = int(run)
        rand.seed(seed)

        self.__repository.createPopulation(args=[POPULATION_SIZE, INDIVIDUAL_SIZE])
        onePopulation, populationFitness = self.run()
        return self.__repository.getBestPath(), onePopulation, populationFitness

    def load_map(self, val):
        if val == "random":
            self.__repository.loadRandomMap()
        else:
            self.__repository.load_file(val)
        self.mapChanged()

    def getMap(self):
        return self.__repository.getMap()

    def mapChanged(self):
        self.__currentIteration = 0

    def __stopCondition(self):
        if self.__currentIteration != MAX_ITERATIONS:
            return True
        return False

























    # def selection(self, population):
    #     individuals = population.getPopulation()
    #     sumFitnessPopulation = population.computeSumFitness()
    #     firstIndex = 0
    #     secondIndex = 0
    #     selected = False
    #     while not selected:
    #         probability = population.getPopulation()[firstIndex].getFitness() / sumFitnessPopulation
    #         if random() < probability:
    #             selected = True
    #         else:
    #             firstIndex += 1
    #             firstIndex = firstIndex % len(population.getPopulation())
    #
    #     selected = False
    #     while not selected:
    #         probability = population.getPopulation()[secondIndex].getFitness() / sumFitnessPopulation
    #         if random() < probability and firstIndex != secondIndex:
    #             selected = True
    #         else:
    #             secondIndex += 1
    #             secondIndex = secondIndex % len(population.getPopulation())
    #
    #     parent1 = individuals[firstIndex]
    #     parent2 = individuals[secondIndex]
    #
    #     offspring1, offspring2 = parent1.crossover(parent2)
    #
    #     offspring1.mutate()
    #     offspring2.mutate()
    #
    #     if offspring1 is None and offspring2 is None:
    #         return  # the crossover was not done because it didn't meet the crossover probability
    #
    #     if offspring1.getFitness() > offspring2.getFitness():
    #         population.addIndividual(offspring1)
    #
    #     else:
    #         population.addIndividual(offspring2)

















    # def iteration(self, nrOfSelections, population):
    #     # args - list of parameters needed to run one iteration
    #     # a iteration:
    #     # selection of the parrents
    #     # create offsprings by crossover of the parents
    #     # apply some mutations
    #     # selection of the survivors
    #
    #     for index in range(nrOfSelections):
    #         self.selection(population)
    #
    #     population.evaluate()
    #     population.selection()


    # def run(self, cSeed, popSize, genCount, nrOfSelections):
    #     # args - list of parameters needed in order to run the algorithm
    #
    #     # until stop condition
    #     #    perform an iteration
    #     #    save the information needed for the statistics
    #
    #     # return the results and the info for statistics
    #
    #     averages = []
    #
    #     bestIndividual = None
    #     average = 0
    #
    #     for g in range(genCount):
    #         self.iteration(population)
    #
    #         popFitness = []
    #         for p in population.getPopulation():
    #             popFitness.append(p.getFitness())
    #
    #         bestIndividual = population.selection(1)[0]
    #         average = np.average(popFitness)
    #         averages.append(average)
    #
    #     return averages, bestIndividual
    #
    # def solver(self, popSize, indSize, genCount, nrIterations, lastSeed=10):
    #     # args - list of parameters needed in order to run the solver
    #
    #     # create the population,
    #     # run the algorithm
    #     # return the results and the statistics
    #
    #     bestIndividuals = []
    #     averages = []
    #     popFitness = []
    #
    #     rand.seed(cSeed)
    #     population = Population(self.__repository.getDrone(), self.__repository.getMap(), popSize, indSize)
    #     self.__repository.addPopulation(population)
    #
    #     for i in range(lastSeed):
    #         best, avg, popfitness = self.run(i, popSize, indSize, genCount, nrIterations)
    #         print(str(i) + "      " + str(avg) + "      " + str(best.getFitness()))
    #         bestIndividuals.append(best)
    #         averages.append(avg)
    #         popFitness.append(popfitness)
    #
    #     return bestIndividuals, averages, popFitness