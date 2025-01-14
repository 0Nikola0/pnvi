import pygame
from pygame import Surface
from pygame.time import Clock

import settings
from screens import Screen
from hooks import EventHook
from buttons import RestartButton, ExitButton, MenuButton


class EndScreen(Screen):
    def __init__(self, surface: Surface, clock: Clock, hook: EventHook) -> None:
        super().__init__(surface, clock, hook)

        self.background = pygame.image.load("assets/backgrounds/background.png").convert()
        self.background = pygame.transform.scale(self.background, (settings.WINDOWWIDTH, settings.WINDOWHEIGHT))

        brighten = 128
        self.background.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_SUB) 

        btn_size = 50, 50
        btn_posx = settings.WINDOWWIDTH / 2 - btn_size[0] - 120
        btn_marginy = 10

        self.buttons = (
            RestartButton((btn_posx, settings.WINDOWHEIGHT / 3 + 50 - btn_size[1] - btn_marginy), btn_size, "Restart", "assets/buttons/restart.png", hook, color=settings.WHITE),
            MenuButton((btn_posx, settings.WINDOWHEIGHT / 3 + 50), btn_size, "Main Menu", "assets/buttons/menu.png", hook, color=settings.WHITE),
            ExitButton((btn_posx, settings.WINDOWHEIGHT / 3 + 50 + btn_size[1] + btn_marginy), btn_size, "Exit", "assets/buttons/exit2.png", hook, color=settings.WHITE),
        )

    
    def run(self) -> None:
        for event in pygame.event.get():
            Screen.handle_exit(event)

            if event.type == pygame.constants.MOUSEBUTTONUP:
                for b in self.buttons:
                    b.handle_click(event.pos)
        
        self.draw()

    def draw(self) -> None:
        self.surface.blit(self.background, (0, 0))

        for btn in self.buttons:
            btn.draw(self.surface)

            if settings.DEBUG:
                btn.debug_draw(self.surface)
        
        pygame.display.update()
