import pygame
from Domain.constants import *
from controller import *
from random import randint
import time

class GUI:

    def __init__(self):
        # We position on a random area on the map the drone
        self.__initialX = randint(START, END)
        self.__initialY = randint(START, END)
        # self.__initialX = 14
        # self.__initialY = 5
        # self.__finalX = 0
        # self.__finalY = 1

        # We get the final coordinates for the drone
        self.__finalX = randint(START, END)
        self.__finalY = randint(START, END)
        self.__controller = Controller(self.__initialX, self.__initialY)

    def start(self):

        # initialize the pygame module
        pygame.init()

        # load and set the logo
        # self.__controller.getMap().loadMap("test1.map")
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple envitonment")

        # create a surface on screen that has the size of 400 x 400
        screen = pygame.display.set_mode((1200, 400))
        screen.fill(WHITE)

        # check whether the end point is a wall
        while self.__controller.getMap().surface[self.__finalX][self.__finalY] == 1:
            self.__finalX = randint(START, END)
            self.__finalY = randint(START, END)

        print('Start: (' + str(self.__initialX) + ', ' + str(self.__initialY) + ')')
        print('End: (' + str(self.__finalX) + ', ' + str(self.__finalY) + ')')

        # define a variable to control the main loop
        running = True

        # variables for printing the Path
        printedTime = False
        printedG = False
        printedA = False
        printedD = False

        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False


            startG = time.time()
            pathG = self.__controller.searchGreedy(self.__initialX, self.__initialY, self.__finalX, self.__finalY)
            endG = time.time()
            if len(pathG) == 0:
                print('Path does not exit!')
                return

            if not printedG:
                print('Greedy Path: ')
                print(pathG)
                printedG = True
            screen.blit(self.__controller.displayWithPath(self.__controller.getMap().image(BLUE), pathG, PALEBLUE), (0, 0))

            startA = time.time()
            pathA = self.__controller.searchAStar(self.__initialX, self.__initialY, self.__finalX, self.__finalY)
            endA = time.time()
            if len(pathA) == 0:
                print('Path does not exist!')
                return

            if not printedA:
                print('A* Path: ')
                print(pathA)
                printedA = True
            screen.blit(self.__controller.displayWithPath(self.__controller.getMap().image(PINK_2), pathA, PALEPINK), (400, 0))


            startD = time.time()
            pathD = self.__controller.searchDFS(self.__initialX, self.__initialY, self.__finalX, self.__finalY)
            endD = time.time()
            if len(pathD) == 0:
                print('Path does not exist!')
                return

            if not printedD:
                print('DFS Path: ')
                print(pathD)
                printedD = True

            screen.blit(self.__controller.displayWithPath(self.__controller.getMap().image(GREEN), pathD, PALEGREEN), (800, 0))

            if not printedTime:
                print('\nExecution time for Greedy: ' + str(endG - startG))
                print('Execution time for A*: ' + str(endA - startA))
                print('Execution time for DFS: ' + str(endD - startD))
                printedTime = True

            pygame.display.flip()
        pygame.quit()