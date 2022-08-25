import pygame


class Drone:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        # the stack is used for DFS
        self.stack = [(self.x, self.y)]
        self.visited = []

    def getX(self):
        return self.x

    def setX(self, newX):
        self.x = newX

    def getY(self):
        return self.y

    def setY(self, newY):
        self.y = newY

    def getStack(self):
        return self.stack

    def getVisited(self):
        return self.visited


