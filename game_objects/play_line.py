import pygame

import settings


class PlayLine:
    def __init__(self, pos) -> None:
        size = (settings.LINE_WIDTH, settings.WINDOWHEIGHT)
        self.rect = pygame.Rect(pos, size)
