import pygame
import pygame.font
import pygame.locals

import settings
from screens import PlayScreen


def main():
    global DISPLAYSURF, PLAY_BOARD

    pygame.init()
    pygame.display.set_caption('Laboratoriska Game')

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((settings.WINDOWWIDTH, settings.WINDOWHEIGHT))

    PLAY_SCREEN = PlayScreen(DISPLAYSURF)

    while True:

        PLAY_SCREEN.draw()

        pygame.display.update()
        FPSCLOCK.tick(settings.FPS)


if __name__ == "__main__":
    main()
