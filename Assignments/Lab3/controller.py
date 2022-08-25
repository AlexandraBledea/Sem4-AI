import pygame

from Domain.map import Map
from Domain.constants import *
from Domain.drone import Drone

class Controller:

    def __init__(self, x, y):
        self.__map = Map()
        self.__drone = Drone(x, y)

    def getMap(self):
        return self.__map

    def getDrone(self):
        return self.__drone

    def getDroneX(self):
        return self.__drone.getX()

    def getDroneY(self):
        return self.__drone.getY()


    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()

        if self.__drone.x > 0:
            if pressed_keys[pygame.K_UP] and detectedMap.surface[self.getDroneX() - 1][self.getDroneY()] == 0:
                self.__drone.setX(self.getDroneX() - 1)

        if self.getDroneX() < 19:
            if pressed_keys[pygame.K_DOWN] and detectedMap.surface[self.getDroneX() + 1][self.getDroneY()] == 0:
                self.__drone.setX(self.getDroneX() + 1)

        if self.getDroneY() > 0:
            if pressed_keys[pygame.K_LEFT ]and detectedMap.surface[self.getDroneX()][self.getDroneY() - 1] == 0:
                self.__drone.setY(self.getDroneY() - 1)

        if self.getDroneY() < 19:
            if pressed_keys[pygame.K_RIGHT] and detectedMap.surface[self.getDroneX()][self.getDroneY() + 1] == 0:
                self.__drone.setY(self.getDroneY() + 1)

    def validNode(self, x, y):
        return -1 < x < 20 and -1 < y < 20 and self.__map.surface[x][y] == 0

    def heuristicManhattanDistance(self, x1, x2, y1, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def buildPath(self, previous, finalX, finalY):
        path = [(finalX, finalY)]
        coord = previous[(finalX, finalY)]
        while coord != (None, None):
            path.append(coord)
            coord = previous[coord]

        path.reverse()
        return path

    def searchDFS(self, initialX, initialY, finalX, finalY):
        found = False
        visited = []

        visitStack = [(initialX, initialY)]

        previous = dict()
        previous[(initialX, initialY)] = (None, None)

        while visitStack and not found:
            node = visitStack.pop(0)
            visited.append(node)

            if node == (finalX, finalY):
                found = True
            else:
                for d in directions:
                    newX = node[0] + d[0]
                    newY = node[1] + d[1]

                    if self.validNode(newX, newY) and (newX, newY) not in visited:
                        previous[(newX, newY)] = node
                        visited.append((newX, newY))
                        visitStack.insert(0, (newX, newY))

        if found:
            return self.buildPath(previous, finalX, finalY)
        else:
            return []

    def searchAStar(self, initialX, initialY, finalX, finalY):
        # TO DO
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y]

        found = False
        visited = []
        visitQueue = [(initialX, initialY)]
        previous = dict()
        previous[(initialX, initialY)] = (None, None)
        nrOfSteps = dict()
        nrOfSteps[(initialX, initialY)] = 0

        while visitQueue and not found:
            node = visitQueue.pop(0)
            visited.append(node)

            if node == (finalX, finalY):
                found = True
            else:
                aux = []
                for d in directions:
                    newX = node[0] + d[0]
                    newY = node[1] + d[1]

                    if self.validNode(newX, newY) and (newX, newY) not in visited:
                        if (newX, newY) not in visitQueue:
                            aux.append((newX, newY))
                            previous[(newX, newY)] = node
                            nrOfSteps[(newX, newY)] = nrOfSteps[node] + 1
                        else:
                            if nrOfSteps[(newX, newY)] > nrOfSteps[node] + 1:
                                visitQueue.remove((newX, newY))
                                aux.append((newX, newY))
                                previous[(newX, newY)] = node
                                nrOfSteps[(newX, newY)] = nrOfSteps[node] + 1
                visitQueue.extend(aux)
                visitQueue.sort(key=lambda coord: self.heuristicManhattanDistance(coord[0], finalX, coord[1], finalY) + nrOfSteps[coord])

        if found:
            return self.buildPath(previous, finalX, finalY)
        else:
            return []

    def searchGreedy(self, initialX, initialY, finalX, finalY):
        # TO DO
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y]

        found = False  # We mark if the final node was found or not
        visited = []  # We mark the visited nodes
        previous = dict()  # We keep the evidence of all the previous nodes passed by
        previous[(initialX, initialY)] = (None, None)  # For the initial node, there is no previous
        visitQueue = [(initialX, initialY)]  # We add the initial node to the Visit Queue
        while visitQueue and not found:
            node = visitQueue.pop(0)
            visited.append(node)  # We mark the current node as being visited

            if node == (finalX, finalY):  # If the current node is the final node, we mark that we found it
                found = True
            else:
                # Otherwise we go through the unvisited neighbors of the current node
                aux = []
                for d in directions:
                    newX = node[0] + d[0]
                    newY = node[1] + d[1]

                    # We check if the node is valid
                    if self.validNode(newX, newY) and (newX, newY) not in visited:
                        aux.append((newX, newY))
                        previous[(newX, newY)] = node

                # We add the neighbors to the toVisitQueue
                visitQueue.extend(aux)
                # We sort the queue based on the ManhattanDistance rule
                visitQueue.sort(key=lambda coord: self.heuristicManhattanDistance(coord[0], finalX, coord[1], finalY))

        if found:
            return self.buildPath(previous, finalX, finalY)
        else:
            return []

    def dummysearch(self):
        # example of some path in test1.map from [5,7] to [7,11]
        return [[5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [6, 11], [7, 11]]

    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("drona.png")
        mapImage.blit(drona, (self.getDroneX() * 20, self.getDroneY() * 20))

        return mapImage

    def displayWithPath(self, image, path, color):
        mark = pygame.Surface((20, 20))
        mark.fill(color)
        for move in path:
            image.blit(mark, (move[0] * 20, move[1] * 20))

        return image
