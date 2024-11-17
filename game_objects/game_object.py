import pygame

class GameObject:
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int]) -> None:
        self.color = color
        self.rect = pygame.Rect(pos, size)

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
