import pygame
from Domain.constants import *
from controller import *
from random import randint
import time

class GUI:

    def __init__(self):
        # We position on a random area on the map the drone
        # x = randint(START, END)
        x = 2
        y = 4
        # y = randint(START, END)
        self.__controller = Controller(x, y)


    def initializeMainScreen(self):
        screen = pygame.display.set_mode(MAIN_WINDOW)
        screen.fill(WHITE)

        screen.blit(self.__controller.getEnvironment().image(), FULL_BLIT)
        pygame.display.flip()
        return screen


    def initializeStartScreen(self):
        screen = pygame.display.set_mode(START_WINDOW)
        screen.fill(WHITE)

        # add background image
        background = pygame.image.load("nyanstart2.png")
        screen.blit(background, FULL_BLIT)

        # add font
        pygame.font.init()
        font = pygame.font.SysFont('comicsans', START_FONT)
        image = font.render('Explore the galaxy!', True, NAVYBLUE)

        # draw the button
        pygame.draw.rect(screen, WHITE, POSITION_BUTTON, border_radius = BORDER)
        pygame.draw.rect(screen, BLACK, POSITION_BUTTON, 2, border_radius= BORDER)
        screen.blit(image, BLIT_START_FONT)
        pygame.display.flip()
        return screen


    def initializeGame(self):

        # initialize the pygame module
        pygame.init()

        # load and set the logo
        logo = pygame.image.load("nyanlogo.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Interstellar travel")

        # add music
        pygame.mixer.init()
        pygame.mixer.music.load("nyan.mp3")
        pygame.mixer.music.play(MUSIC_REPEAT, MUSIC_REPEAT)


    def start(self):

        self.initializeGame()
        screen = self.initializeStartScreen()

        start = True
        runningMain = False

        # start screen
        while start:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    start = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if START_BUTTON <= pygame.mouse.get_pos()[MOUSE_WIDTH_POS] <= END_BUTTON_WIDTH:
                        if START_BUTTON <= pygame.mouse.get_pos()[MOUSE_HEIGHT_POS] <= END_BUTTON_HEIGHT:
                            # Exist the current loop and enter the MAIN WINDOW
                            screen = self.initializeMainScreen()
                            runningMain = True
                            start = False


        # main screen
        while runningMain:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    runningMain = False

            # We move the spaceship one step using DFS
            self.__controller.moveDSF()
            time.sleep(SLEEP)

            if self.__controller.getDroneX() is None and self.__controller.getDroneY() is None:
                runningMain = False
            else:
                self.__controller.markDetectedWalls()
                screen.blit(self.__controller.getDMapImage(), DMAP_BLIT)
                pygame.display.flip()

        pygame.quit()

