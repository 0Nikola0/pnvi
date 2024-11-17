import random
import pygame

import settings
from screens import Screen
from game_objects import Actor, GameObject, Pedastel, PlayLine


DEBUG = True


class PlayScreen(Screen):
    def __init__(self, surface) -> None:
        self.surface = surface
        
        self.play_lines = tuple(
            PlayLine((settings.LINE_WIDTH * i, 0)) for i in range(0, 5)
        )

        self.player = Actor(self.play_lines)
        self.pedastels = []
        self.objects: list[GameObject] = []


        self.build_scene()
        
        if DEBUG:
            self.set_debug_lines()

    def draw(self):

        # TODO events ne se za u draw() funkc
        for event in pygame.event.get():
            Screen.handle_exit(event)

            if event.type == pygame.constants.MOUSEBUTTONUP:
                self.player.handle_mouse(event.pos)
            
            elif event.type == pygame.constants.KEYDOWN:
                self.player.handle_keyboard(event.key)
                if DEBUG:
                    self.handle_debug_keys(event.key)



        # UPDATE
        self.player.update(self.pedastels)

        self.surface.fill(settings.BGCOLOR)
        for object in self.objects:
            object.draw(self.surface)
            
        if DEBUG:
            self.debug_draw()

        pygame.display.update()

    def build_scene(self):
        def is_valid_line(line):
            return line >= 0 and line < 5
        
        current_line = 2
        directions = (-1, +1)

        self.pedastels = []

        for i in range(10):
            self.pedastels.append(Pedastel(current_line))

            direction = random.choice(directions)
            if is_valid_line(current_line + direction):
                current_line += direction
            else:
                current_line -= direction
        
        self.refresh_objects()

    def refresh_objects(self):
        self.objects = [*self.pedastels, self.player]

    # -------- DEBUG ------- #
    def set_debug_lines(self):
        self.debug_lines = (
            (settings.LINE_WIDTH, 0),
            (settings.LINE_WIDTH, settings.WINDOWHEIGHT),
            (settings.LINE_WIDTH * 2, 0),
            (settings.LINE_WIDTH * 2, settings.WINDOWHEIGHT),
            (settings.LINE_WIDTH * 3, 0),
            (settings.LINE_WIDTH * 3, settings.WINDOWHEIGHT),
            (settings.LINE_WIDTH * 4, 0),
            (settings.LINE_WIDTH * 4, settings.WINDOWHEIGHT),
        )

    def debug_draw(self):
        # pygame.draw.lines(self.surface, settings.WHITE, False, self.debug_lines)
        for i in self.play_lines:
            pygame.draw.rect(self.surface, (255, 255, 255), i.rect, 3)

    def handle_debug_keys(self, key):
        if key == pygame.constants.K_g:
            Pedastel.reset_height()
            self.build_scene()
        elif key == pygame.constants.K_r:
            self.player.debug_reset_position()