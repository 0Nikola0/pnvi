import pygame
from pygame import Surface
from pygame.time import Clock

import settings
from screens import Screen
from game_objects import Coin
from hooks import EventHook, StaticHook
from buttons import SkinButton, CheckButton, Button


class ShopScreen(Screen):
    def __init__(self, surface: Surface, clock: Clock, hooks: dict[EventHook]) -> None:
        super().__init__(surface, clock, hooks["screen_hook"])

        self.background = pygame.transform.scale(
            surface = pygame.image.load("assets/backgrounds/sky_background.png").convert(), 
            size = (settings.WINDOWWIDTH, settings.WINDOWHEIGHT)
        )

        btn_size = 75, 75
        btn_margin = settings.WINDOWWIDTH / 10, settings.WINDOWHEIGHT / 8
        self.buttons: list[Button] = [
            CheckButton((20, 20), (40, 40), "assets/buttons/check.png", hooks["screen_hook"]),

            SkinButton((settings.WINDOWWIDTH / 2 - btn_size[0] - btn_margin[0], settings.WINDOWHEIGHT / 2 - btn_size[1] - btn_margin[1]),
                btn_size, hooks["skin_hook"], "Lila", 1, "assets/characters/Monster_lila.png"),
            SkinButton((settings.WINDOWWIDTH / 2 + btn_margin[0], settings.WINDOWHEIGHT / 2 - btn_size[1] - btn_margin[1]),
                btn_size, hooks["skin_hook"], "Blau", 2, "assets/characters/Monster_blau.png"),
            SkinButton((settings.WINDOWWIDTH / 2 - btn_size[0] - btn_margin[0], settings.WINDOWHEIGHT / 2 + btn_margin[1] - 24),
                btn_size, hooks["skin_hook"], "Gruen", 3, "assets/characters/Monster_gruen.png"),
            SkinButton((settings.WINDOWWIDTH / 2 + btn_margin[0], settings.WINDOWHEIGHT / 2 + btn_margin[1] - 24),
                btn_size, hooks["skin_hook"], "Rot", 15, "assets/characters/Monster_rot.png"),
        ]

        self.font = pygame.font.Font(pygame.font.get_default_font(), 32)
        self.coin_icon = Coin((settings.WINDOWWIDTH - Coin.SIZE[0] - 20, 20))

    def run(self) -> None:
        self.handle_events()
        self.draw()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            Screen.handle_exit(event)

            if event.type == pygame.constants.MOUSEBUTTONUP:
                for btn in self.buttons:
                    if btn.handle_click(event.pos):
                        self.restart()

    def draw(self) -> None:
        self.surface.fill(settings.BGCOLOR)
        self.surface.blit(self.background, (0, 0))
        self.draw_coins()

        for btn in self.buttons:
            btn.draw(self.surface)

            if settings.DEBUG:
                btn.debug_draw(self.surface)
        
        pygame.display.update()

    def draw_coins(self) -> None:
        text_surface = self.font.render(str(StaticHook.read_data().get("coins", 0)), True, (0, 0, 0))
        text_rect = text_surface.get_rect(right=self.coin_icon.rect.left - 10, centery=self.coin_icon.rect.centery + 4)
        self.surface.blit(text_surface, text_rect)
        self.coin_icon.draw(self.surface)

    def restart(self) -> None:
        for btn in self.buttons:
            btn.refresh()
