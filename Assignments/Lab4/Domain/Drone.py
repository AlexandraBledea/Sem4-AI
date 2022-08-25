
class Drone:
    def __init__(self, x, y, battery: object = 20) -> object:
        self.__x = x
        self.__y = y
        self.__battery = battery

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getBattery(self):
        return self.__battery