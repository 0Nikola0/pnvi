from __future__ import annotations

import pygame
from random import randint

import settings
from .coin import Coin
from .game_object import GameObject


class Pedastel(GameObject):
    MARGIN_X, MARGIN_Y = 10, 5
    GAP_Y = 50
    SIZE = (settings.LINE_WIDTH - MARGIN_X * 2, 15)
    CURRENT_HEIGHT = settings.WINDOWHEIGHT
    BOTTOM_HEIGHT = CURRENT_HEIGHT - SIZE[1] - MARGIN_Y
    
    def __init__(self, x_index: int, y_index: int, color: tuple[int, int, int] = settings.GREEN) -> None:
        '''
        x_index (int): which line should the pedastel be on (left-right)
        y_index (int): which height should the pedastel be (1-lowest, 8-highest)
        '''
        self.y_index = y_index
        pos = (x_index * settings.LINE_WIDTH + Pedastel.MARGIN_X, 
               Pedastel.BOTTOM_HEIGHT - (Pedastel.SIZE[1] + Pedastel.GAP_Y) * self.y_index - Pedastel.SIZE[1] - Pedastel.MARGIN_Y)
        
        super().__init__(pos, Pedastel.SIZE, color)

        self.wanted_pos = pos[1]
        self.velocity_y = 0
        self.max_speed = 20

        self.sprite = pygame.transform.scale(pygame.image.load("assets/objects/pedastel.png"), Pedastel.SIZE)
        self.coin = self.setup_coin() if randint(1, 7) == 5 else None

    
    def draw(self, surface):
        surface.blit(self.sprite, self.rect)
        if self.coin:
            self.coin.draw(surface)
    

    def calculate_jump(self, by: int = 1) -> None:
        razlika = self.rect.top
        self.wanted_pos = self.rect.top + (Pedastel.SIZE[1] + Pedastel.GAP_Y + Pedastel.MARGIN_Y) * by

        # self.y_index -= by
        # self.rect.top += (Pedastel.SIZE[1] + Pedastel.GAP_Y) * by

        razlika = self.wanted_pos - self.rect.top
        return razlika
    
    def update_index(self, by: int = 1) -> None:
        self.y_index -= by
    
    def update(self, *args, **kwargs) -> None:
        ...
        # if self.rect.top < self.wanted_pos:
        #     if (nv := self.velocity_y + settings.GRAVITY) <= 20 * 0.65:
        #         self.velocity_y = nv
        #     else:
        #         self.velocity_y = self.max_speed * 0.65

        #     self.rect.top += self.velocity_y

        # elif self.rect.top > self.wanted_pos:
        #     if (nv := self.velocity_y - settings.GRAVITY) >= -(20 * 0.65):
        #             self.velocity_y = nv
        #     else:
        #         self.velocity_y = self.max_speed * -(0.65)
        
        # else:
        #     self.velocity_y = 0


    @classmethod
    def reset_height(cls) -> None:
        cls.CURRENT_HEIGHT = settings.WINDOWHEIGHT

    def setup_coin(self) -> Coin:
        return Coin(
            (
                self.rect.centerx - Coin.SIZE[0] / 2,
                self.rect.top - Coin.SIZE[1] - 35,
            )
        )

    def move_down(self, amount) -> None:
        super().move_down(amount)
        if self.coin:
            self.coin.move_down(amount)

    def collect_coin(self, player_rect: pygame.Rect) -> None:
        if self.coin and self.coin.is_collected(player_rect):
            self.coin = None