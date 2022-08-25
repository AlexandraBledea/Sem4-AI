# -*- coding: utf-8 -*-

#Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

#define indexes variations 
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]

#define mapsize 

mapLengh = 20

MAP_LENGTH = 20
POPULATION_SIZE = 100
INDIVIDUAL_SIZE = 8
MAX_ITERATIONS = 60
INITIAL_POSITION = (0, 6)
NUMBER_OF_RUNS = 10

def addDirections(current, dir):
    return current[0] + dir[0], current[1] + dir[1]