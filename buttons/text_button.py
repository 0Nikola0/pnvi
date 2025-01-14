import pygame

from .button import Button
from hooks import EventHook


class TextButton(Button):
    def __init__(
            self,
            pos: tuple[int, int],
            size: tuple[int, int],
            text: str,
            sprite_path: str,
            hook: EventHook,
            color: tuple[int, int, int] = (0, 0, 0)
        ) -> None:
        super().__init__(pos, size, sprite_path, hook)

        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)
        text_pos = pos[0] + size[0] + 10, pos[1] + size[1] / 2
        self.text_surface = self.font.render(str(text), True, color)
        self.text_rect = self.text_surface.get_rect(left=text_pos[0], centery=text_pos[1])

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        surface.blit(self.text_surface, self.text_rect)
