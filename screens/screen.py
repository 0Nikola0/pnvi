import sys
import pygame

from hooks import EventHook


class Screen:
    screen_serial = 0
    
    def __init__(self, surface: pygame.Surface, clock: pygame.time.Clock, screen_hook: EventHook) -> None:
        self._id = Screen._set_id()
        
        self.surface = surface
        self.clock = clock
        self.screen_hook = screen_hook
    
    def draw(self) -> None:
        pygame.display.flip()

    def restart(self) -> None:
        pass

    @staticmethod
    def handle_exit(event) -> None:
        if event.type == pygame.constants.QUIT or (event.type == pygame.constants.KEYUP and event.key in (pygame.constants.K_ESCAPE, pygame.constants.K_q)):
            Screen.exit()    
    
    @staticmethod
    def exit() -> None:
        pygame.quit()
        sys.exit()

    def get_id(self) -> int:
        return self._id

    @classmethod
    def _set_id(cls) -> int:
        Screen.screen_serial += 1
        return Screen.screen_serial
