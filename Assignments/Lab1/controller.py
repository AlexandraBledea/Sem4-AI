import pygame

from Domain.dmap import DMap
from Domain.constants import *
from Domain.drone import Drone
from Domain.environment import Environment


class Controller:

    def __init__(self, x, y):
        self.__environment = Environment()
        self.__dmap = DMap()
        self.__drone = Drone(x, y)

    def getEnvironment(self):
        return self.__environment

    def getDMap(self):
        return self.__dmap

    def getDrone(self):
        return self.__drone

    def getDroneX(self):
        return self.__drone.getX()

    def getDroneY(self):
        return self.__drone.getY()

    def getDroneStack(self):
        return self.__drone.getStack()

    def getDroneVisited(self):
        return self.__drone.getVisited()

    def getDMapImage(self):
        return self.__dmap.image(self.getDroneX(), self.getDroneY(), self.getDroneVisited())

    def markDetectedWalls(self):
        return self.__dmap.markDetectedWalls(self.__environment, self.getDroneX(), self.getDroneY())

    def getEnvironmentImage(self):
        return self.__environment.image()

    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()

        if self.__drone.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.getDroneX() - 1][self.getDroneY()] == 0:
                self.__drone.setX(self.getDroneX() - 1)

        if self.getDroneX() < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.getDroneX() + 1][self.getDroneY()] == 0:
                self.__drone.setX(self.getDroneX() + 1)

        if self.getDroneY() > 0:
            if pressed_keys[K_LEFT ]and detectedMap.surface[self.getDroneX()][self.getDroneY() - 1] == 0:
                self.__drone.setY(self.getDroneY() - 1)

        if self.getDroneY() < 19:
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.getDroneX()][self.getDroneY() + 1] == 0:
                self.__drone.setY(self.getDroneY() + 1)

    def moveDSF(self):

        # We mark the current position as being visited
        self.__drone.visited.append((self.__drone.x, self.__drone.y))

        # The order will be UP - LEFT - DOWN - RIGHT
        for position in directions:
            new_X = self.__drone.x + position[0]
            new_Y = self.__drone.y + position[1]
            # We check if the drone stays within the map (it doesn't exceed the coordinates 0 20)
            if -1 < new_X < 20 and -1 < new_Y < 20:
                # We check if we don't hit any walls
                if self.__dmap.surface[new_X][new_Y] == 0:
                        # We check if we have not visited this square before
                        if (new_X, new_Y) not in self.__drone.visited:
                            # We add the current position to the stack as well so we can trace it when the drone gets stuck
                            self.__drone.stack.append((self.__drone.x, self.__drone.y))
                            # We add the next position
                            self.__drone.stack.append((new_X, new_Y))
                            break

        # When the stack is empty, x and y will be None and exection will be stopped!
        if not self.__drone.stack:
            self.__drone.x = None
            self.__drone.Y = None

        else:
            # We get the next position
            currentPosition = self.__drone.stack.pop()
            self.__drone.x = currentPosition[0]
            self.__drone.y = currentPosition[1]