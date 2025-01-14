import pygame

import settings


class GameObject(pygame.sprite.Sprite):
    GAME_SPEED = 10
    
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int] = settings.YELLOW) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.rect = pygame.Rect(pos, size)

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)

    def move_down(self, amount) -> None:
        if amount > 0:
            self.rect.top += GameObject.GAME_SPEED