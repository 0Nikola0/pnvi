import pygame
from pygame import Surface
from pygame.time import Clock

import settings
from screens import Screen
from hooks import EventHook
from buttons import PlayButton, ExitButton, ShopButton


class MenuScreen(Screen):
    def __init__(self, surface: Surface, clock: Clock, hook: EventHook) -> None:
        super().__init__(surface, clock, hook)

        self.background = pygame.image.load("assets/backgrounds/background.png").convert()
        self.background = pygame.transform.scale(self.background, (settings.WINDOWWIDTH, settings.WINDOWHEIGHT))

        btn_size = 50, 50
        btn_posx = settings.WINDOWWIDTH / 2 - btn_size[0] - 120
        btn_marginy = 10
        self.buttons = (
            PlayButton((btn_posx, settings.WINDOWHEIGHT / 3 + 50 - btn_size[1] - btn_marginy), btn_size, "Play", "assets/buttons/play.png", hook),
            ShopButton((btn_posx, settings.WINDOWHEIGHT / 3 + 50), btn_size, "Shop", "assets/buttons/shop.png", hook),
            ExitButton((btn_posx, settings.WINDOWHEIGHT / 3 + 50 + btn_size[1] + btn_marginy), btn_size, "Exit", "assets/buttons/exit2.png", hook),
        )
    
    def run(self) -> None:
        self.handle_events()
        self.draw()


    def handle_events(self) -> None:
        for event in pygame.event.get():
            Screen.handle_exit(event)

            if event.type == pygame.constants.MOUSEBUTTONUP:
                for b in self.buttons:
                    b.handle_click(event.pos)


    def draw(self) -> None:
        self.surface.fill(settings.BGCOLOR)
        self.surface.blit(self.background, (0, 0))

        for btn in self.buttons:
            btn.draw(self.surface)

            if settings.DEBUG:
                btn.debug_draw(self.surface)
        
        pygame.display.update()
