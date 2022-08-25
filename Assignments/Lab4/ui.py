# -*- coding: utf-8 -*-


# imports
from gui import *
from controller import *
from repository import *
from Domain.Drone import Drone
import random as rand

from Domain.Map import Map
from Domain.Population import Population
# import matplotlib.pyplot as plot
import matplotlib.pyplot as pympl
from controller import *


# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls


class UI:
    def __init__(self):
        self.__drone = Drone(INITIAL_POSITION[0], INITIAL_POSITION[1])
        self.__service = controller(self.__drone)
        self.path = []
        self.fitness = []
        self.population = []

    @staticmethod
    def print_menu():
        print("0. Exit")
        print("Map options")
        print("1. Create a random map")
        print("2. Load a map")
        print("3. Save map")
        print("4. Visualise map")
        print("-----------------")
        print("5. Parameters setup")
        print("6. Run solver")
        # print("7. View the drone moving on a path")

    def create_random_map(self):
        self.__service.getMap().randomMap([INITIAL_POSITION])
        self.__service.getMap().saveMap("map.map")

    def load_map(self):
        file = input("file: ")
        self.__service.getMap().loadMap(file)
        self.__service.getMap().saveMap("map.map")

    def save_map(self):
        file = input("file: ")
        self.__service.getMap().saveMap(file)


    def view_map(self):
        screen = initPyGame((self.__service.getMap().n * 20, self.__service.getMap().m * 20))
        for i in range(20):
            screen.blit(image(self.__service.getMap()), (0, 0))
        pygame.display.flip()
        pygame.time.wait(5000)
        closePyGame()

    def parameters_setup(self):
        INDIVIDUAL_SIZE = int(input("Battery capacity: "))
        MAX_ITEARIONS = int(input("Max iterations: "))
        POPULATION_SIZE = int(input("Population size: "))

    def run_solver(self):

        bestFitnesses = []
        for run in range(NUMBER_OF_RUNS):
            self.path, self.population, self.fitnesses = self.__service.solver(run)
            print("Best fitness: ", self.population.bestFitness())
            pympl.plot(self.fitnesses)
            bestFitnesses.append(self.population.bestFitness())

        pympl.savefig("avg_fitness_variation_runs.png")
        print("AVG: " + str(np.average(bestFitnesses)))
        print("STDDEV: " + str(np.std(bestFitnesses)))

    def view_moving_drone(self):
        print("path: ", self.path)
        movingDrone(self.__service.getMap(), self.path, 4)

    def start(self):
        done = False
        while not done:
            UI.print_menu()
            ch = int(input("Choice: "))
            if ch == 0:
                done = True
            elif ch == 1:
                self.create_random_map()
            elif ch == 2:
                self.load_map()
            elif ch == 3:
                self.save_map()
            elif ch == 4:
                self.view_map()
            elif ch == 5:
                self.parameters_setup()
            elif ch == 6:
                self.run_solver()
            elif ch == 7:
                self.view_moving_drone()



























# class UI:
#
#     def __init__(self):
#         self.__controller = controller()
#         self.__bestIndividuals = []
#         self.__populationSize = 50
#         self.__individualsSize = 30
#         self.__generationsCount = 20
#         self.__numberOfIterations = 100
#
#     def __printMenu(self):
#         print("\n1. Map options")
#         print("2. EA options")
#         print("0. Exit")
#
#     def __printMenuMap(self):
#         print("\nMap options:")
#         print("1. Generate random map")
#         print("2. Load map")
#         print("3. Save map")
#         print("4. Visualize map")
#         print("0. Exit")
#
#     def __printMenuEA(self):
#         print("\nEA options:")
#         print("1. Parameters setup")
#         print("2. Run the solver")
#         print("3. View the drone moving on a path")
#         print("0. Exit")
#
#     def plotGraph(self, solutionAverages):
#         plot.plot(solutionAverages)
#         plot.savefig("solutionAverageFitness.png")
#
#     def logToFile(self, solutionAverages, lastSeed=30, populationSize=50, individualsSize=30, generationCount=30,
#                   numberIterations=50):
#         logFile = open("results.txt", "a")
#         logFile.write("Seeds = [%d, %d]; " % (1, lastSeed))
#         logFile.write(
#             "Pop.size = %d; Ind.size = %d; Generations = %d; " % (populationSize, individualsSize, generationCount))
#         logFile.write(
#             "Iterations/gen = %d; Mutation prob = %.2f; Crossover prob = %.2f\n" % (numberIterations, 0.04, 0.8))
#         logFile.write("Average of averages: %.3f\n" % np.average(solutionAverages))
#         logFile.write("Stdev of averages: %.3f\n" % np.std(solutionAverages))
#         logFile.write("\n")
#         logFile.close()

# -*- coding: utf-8 -*-


# imports
# from gui import *
# from controller import *
# from Domain import *
# import matplotlib.pyplot as plot


# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes through walls

























# class UI:
#     def __init__(self):
#         self.__controller = controller()
#         self.__bestIndividuals = []
#         #popSize=50, indSize=30, genCount=20, nrIterations=100
#         self.__popSize = 50
#         self.__indSize = 30
#         self.__genCount = 20
#         self.__nrIterations = 100
#
#     def __printMenu(self):
#         print("\n1. Map options")
#         print("2. EA options")
#         print("0. Exit")
#
#     def __printMenuMap(self):
#         print("\nMap options:")
#         print("1. Generate random map")
#         print("2. Load map")
#         print("3. Save map")
#         print("4. Visualize map")
#         print("0. Exit")
#
#     def __printMenuEA(self):
#         print("\nEA options:")
#         print("1. Parameters setup")
#         print("2. Run the solver")
#         print("3. View the drone moving on a path")
#         print("0. Exit")
#
#     def plotGraph(self, solutionAverages):
#         plot.plot(solutionAverages)
#         plot.savefig("solutionAverageFitness.png")
#
#     def logToFile(self, solutionAverages, popFitness, lastSeed=30, populationSize=50, individualSize=30, generationCount=30,
#                   numberIterations=50):
#         logFile = open("results.txt", "a")
#         logFile.write("Seeds = [%d, %d]; " % (1, lastSeed))
#         logFile.write(
#             "Pop.size = %d; Ind.size = %d; Generations = %d; " % (populationSize, individualSize, generationCount))
#         logFile.write(
#             "Iterations/gen = %d; Mutation prob = %.2f; Crossover prob = %.2f\n" % (numberIterations, 0.04, 0.8))
#         logFile.write("Average of averages: %.3f\n" % np.average(solutionAverages))
#         logFile.write("Stdev of averages: %.3f\n" % np.std(popFitness))
#         logFile.write("\n")
#         logFile.close()
#
#     def runMap(self):
#         newMap = Map()
#         while True:
#             self.__printMenuMap()
#             mapOption = input("Your option: ")
#
#             if mapOption == "1":
#                 newMap.randomMap()
#                 print("Map successfully generated!\n")
#
#             elif mapOption == "2":
#                 mapName = input("Enter the map filename: ")
#                 newMap.loadMap(mapName)
#                 print("Map successfully loaded!\n")
#
#             elif mapOption == "3":
#                 mapName = input("Enter the map filename: ")
#                 newMap.saveMap(mapName)
#                 print("Map successfully saved!\n")
#
#             elif mapOption == "4":
#                 print(newMap)
#
#             elif mapOption == "0":
#                 break
#
#             else:
#                 print("Invalid command.\n")
#
#         self.__controller.setMap(newMap)
#
#     def runEA(self):
#         while True:
#             self.__printMenuEA()
#             eaOption = input("Your option: ")
#
#             if eaOption == "1":
#                 self.__popSize = input("Population size: ")
#                 self.__indSize = input("Number of individuals: ")
#                 self.__genCount = input("Number of generations: ")
#                 self.__nrIterations = input("Number of iterations: ")
#
#             elif eaOption == "2":
#                 bestIndividuals, averages, popFitness = self.__controller.solver(self.__popSize, self.__indSize, self.__genCount, self.__nrIterations)
#                 bestIndividuals.sort(key=lambda e: e.getFitness(), reverse=True)
#                 self.__bestIndividuals = bestIndividuals[:3]
#                 self.plotGraph(averages)
#                 self.logToFile(averages, popFitness)
#
#             elif eaOption == "3":
#                 screen = initPyGame((400, 400))
#                 movingDrone(screen, self.__controller, self.__bestIndividuals)
#                 closePyGame()
#
#             elif eaOption == "0":
#                 break
#
#             else:
#                 print("Invalid command.\n")
#
#     def run(self):
#         while True:
#             self.__printMenu()
#             option = input("Your option: ")
#
#             if option == "1":
#                 self.runMap()
#             elif option == "2":
#                 self.runEA()
#             elif option == "0":
#                 break
#             else:
#                 print("Invalid command.\n")
