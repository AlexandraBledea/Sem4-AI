import pygame
from domain.constants import Constants


class GUI:

    def __init__(self, controller):
        pygame.init()
        self._screen = pygame.display.set_mode((400, 400))
        self._screen.fill(Constants.WHITE)
        self._controller = controller

    def get_map_image(self, surface, color=Constants.PALE_GREEN, background=Constants.PALE_YELLOW):
        image = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        sensor = pygame.Surface((20, 20))
        accessible = pygame.Surface((20, 20))

        brick.fill(color)
        image.fill(background)
        sensor.fill(Constants.PALE_PINK)
        accessible.fill(Constants.PALE_PURPLE)

        for i in range(Constants.MAP_SIZE):
            for j in range(Constants.MAP_SIZE):

                if surface[i][j] == 1:
                    image.blit(brick, (j * 20, i * 20))
                elif surface[i][j] == 3:
                    image.blit(sensor, (j * 20, i * 20))
                elif surface[i][j] == 2:
                    image.blit(accessible, (j * 20, i * 20))

        return image

    def display_map(self, surface):

        path_image = self.get_map_image(surface)
        self._screen.blit(path_image, (0, 0))
        pygame.display.update()
        return path_image

    def start(self):

        self.display_map(self._controller.map.surface)

        bestSolution = self._controller.run()
        if bestSolution is None:
            print("Failed! No solution found!")

        print("Maximum number of visited positions = " + str(bestSolution.get_evaluation))
        print("Battery left = " + str(bestSolution.left_battery))

        path_order = []

        for sensor in bestSolution.sensor_order:
            path_order.append(str(sensor))

        print("Sensors order: " + str(path_order))

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                else:
                    pygame.event.pump()

                pygame.time.wait(200)