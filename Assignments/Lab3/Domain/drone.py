import pygame


class Drone:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def setX(self, newX):
        self.x = newX

    def getY(self):
        return self.y

    def setY(self, newY):
        self.y = newY


