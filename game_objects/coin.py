from __future__ import annotations

import pygame

from hooks import StaticHook
from .game_object import GameObject
from utils.decorators import on_collision_rect


class Coin(GameObject):
    SIZE = 30, 30
    def __init__(self, pos: tuple[int, int], size: tuple[int, int] = None) -> None:
        size = size or Coin.SIZE
        super().__init__(pos, size)

        self.sprite = pygame.transform.scale(pygame.image.load("assets/objects/coin.png"), size)

    def set_pos(self, pos: tuple[int, int]) -> None:
        '''
        pos: topleft position of the object
        '''
        self.rect.topleft = pos

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.sprite, self.rect)

    @on_collision_rect
    def is_collected(self, player_rect: pygame.Rect) -> bool:
        StaticHook.add_data(
            coins = StaticHook.read_data().get("coins", 0) + 1
        )
        return True