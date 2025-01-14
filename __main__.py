import pygame
import pygame.font
import pygame.locals

import settings
from hooks import EventHook, StaticHook
from screens import PlayScreen, MenuScreen, EndScreen, ShopScreen, Screen

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('PNVI')

        self.FPS_CLOCK = pygame.time.Clock()
        self.DISPLAY_SURF = pygame.display.set_mode((settings.WINDOWWIDTH, settings.WINDOWHEIGHT))

        self.screen_hook = EventHook()
        self.skin_hook = EventHook()

        self.hooks = {
            "screen_hook": self.screen_hook,
            "skin_hook": self.skin_hook,
        }

        self.PLAY_SCREEN = PlayScreen(self.DISPLAY_SURF, self.FPS_CLOCK, self.hooks)
        self.MAIN_MENU_SCREEN = MenuScreen(self.DISPLAY_SURF, self.FPS_CLOCK, self.screen_hook)
        self.END_SCREEN = EndScreen(self.DISPLAY_SURF, self.FPS_CLOCK, self.screen_hook)
        self.SHOP_SCREEN = ShopScreen(self.DISPLAY_SURF, self.FPS_CLOCK, self.hooks)

        StaticHook.add_data(
            play_screen=self.PLAY_SCREEN,
            main_menu_screen=self.MAIN_MENU_SCREEN,
            end_screen=self.END_SCREEN,
            shop_screen=self.SHOP_SCREEN,
        )

        self.current_screen: Screen = self.MAIN_MENU_SCREEN
        self.running = True
    
    def run(self) -> None:
        while self.running:

            if self.screen_hook.check_changes():
                self.current_screen = self.screen_hook.read_data()["current_screen"]
                self.current_screen.restart()

            self.current_screen.run()
            self.FPS_CLOCK.tick(settings.FPS)



if __name__ == "__main__":
    game = Game()
    game.run()
