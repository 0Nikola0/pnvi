import pygame

import settings
from hooks import EventHook


class Button:
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], sprite_path: str, hook: EventHook) -> None:
        self.hook = hook
        self.rect = pygame.Rect(pos, size)
        self.sprite = pygame.transform.scale(
            pygame.image.load(sprite_path).convert_alpha(),
            size
        )

    def handle_click(self, mouse_pos: tuple[int, int]) -> None:
        print("Handle click not implemented")

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.sprite, self.rect)

    def debug_draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, settings.WHITE, self.rect, 3)
    
    def refresh(self) -> None:
        pass
