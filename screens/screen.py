import sys
import pygame


class Screen:
    def __init__(self) -> None:
        raise NotImplementedError
    
    def draw() -> None:
        raise NotImplementedError

    @staticmethod
    def handle_exit(event) -> None:
        if event.type == pygame.constants.QUIT or (event.type == pygame.constants.KEYUP and event.key in (pygame.constants.K_ESCAPE, pygame.constants.K_q)):
            pygame.quit()
            sys.exit()
