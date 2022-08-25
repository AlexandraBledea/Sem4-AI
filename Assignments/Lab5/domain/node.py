class Node:
    def __init__(self, xCoord, yCoord):
        self._x = xCoord  # the coords are valid
        self._y = yCoord

    def x(self):
        return self._x

    def y(self):
        return self._y