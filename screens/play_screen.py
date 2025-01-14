import random
import time
import pygame

import settings
from hooks import EventHook, StaticHook
from screens import Screen
from game_objects import Actor, GameObject, Pedastel, PlayLine


class PlayScreen(Screen):
    GAME_MAX_SPEED = 20 * 0.65
    GAME_SPEED = 2
    
    def __init__(self, surface: pygame.Surface, clock: pygame.time.Clock, hooks: dict[EventHook]) -> None:
        super().__init__(surface, clock, hooks["screen_hook"])
        self.hooks = hooks
        
        self.play_lines: tuple[PlayLine] = tuple(
            PlayLine((settings.LINE_WIDTH * i, 0)) for i in range(0, 5)
        )

        self.current_line = 2

        self.player = Actor(self.play_lines, hooks=hooks)
        self.pedastels: list[Pedastel] = []
        self.objects: list[GameObject] = []

        self.build_scene()

        self.move_down = False
        self.move_down_amount = 0
        self.move_down_velocity = 0

        # pygame.mixer.music.load("assets/sounds/soundtrack.mp3")
        pygame.mixer.music.load("assets/sounds/soundtrack2.mp3")
        # pygame.mixer.music.play(-1)

        self.background = pygame.transform.scale(pygame.image.load("assets/backgrounds/sky_background.png").convert(), (settings.WINDOWWIDTH, settings.WINDOWHEIGHT))

        self.score = 0
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)


    def run(self) -> None:
        for event in pygame.event.get():
            self.handle_events(event)

        if self.move_down:
            if (n := self.move_down_velocity + PlayScreen.GAME_SPEED) < PlayScreen.GAME_MAX_SPEED:
                self.move_down_velocity = n
            else:
                self.move_down_velocity = PlayScreen.GAME_MAX_SPEED
            
            self.draw_screen_moving_down()

            self.player.update(self.pedastels)
            self.move_scene_down(max(self.move_down_velocity, self.amount))

            self.amount -= self.move_down_velocity

            if self.amount <= 0:
                self.move_down = False

        else:
            self.check_coin_collect(self.player.rect)
            if Actor.WENT_UP > 0:
                self.score += Actor.WENT_UP

                self.add_batch_pedastels(Actor.WENT_UP)
                self.refresh_objects()

                for p in self.pedastels:
                    p.update_index(Actor.WENT_UP)

                self.amount = self.pedastels[0].calculate_jump(Actor.WENT_UP)
                
                Actor.WENT_UP = 0
                self.move_down = True
            
            if self.player.is_dead():
                self.end_game()

            self.draw_in_place()

        self.draw()

    def check_coin_collect(self, player_rect: pygame.Rect) -> None:
        for p in self.pedastels:
            p.collect_coin(player_rect)

    def handle_events(self, event):
        Screen.handle_exit(event)
        if event.type == pygame.constants.MOUSEBUTTONUP:
            self.player.handle_mouse(event.pos)
        
        elif event.type == pygame.constants.KEYDOWN:
            self.player.handle_keyboard(event.key)
            if settings.DEBUG:
                self.handle_debug_keys(event.key)

    def draw(self):
        if settings.DEBUG:
            self.debug_draw()

        self.draw_score()
        super().draw()
    
    def draw_in_place(self) -> None:
        self.surface.fill(settings.BGCOLOR)
        self.surface.blit(self.background, (0, 0))

        for object in self.objects:
            object.update(self.pedastels)
            object.draw(self.surface)
    
    def draw_screen_moving_down(self) -> None:
        self.surface.fill(settings.BGCOLOR)
        self.surface.blit(self.background, (0, 0))
        for o in self.objects:
            o.draw(self.surface)
    
    def draw_score(self) -> None:
        text_surface = self.font.render(str(self.score), (10, 10), (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=(10, 10))
        self.surface.blit(text_surface, text_rect)

    def end_game(self) -> None:
        pygame.mixer.music.stop()
        self.player.death_sound.play(0)
        time.sleep(1.5)
        self.screen_hook.set_data(current_screen=StaticHook.read_data()["end_screen"])

    def move_scene_down(self, amount):
        for o in self.objects:
            o.move_down(amount)


    def build_scene(self) -> None:
        self.pedastels = []
        self.add_pedastel(y_index = 1)
        for y_index in range(2, 9):
            self.add_pedastel(y_index=y_index)
        self.refresh_objects()

    def add_pedastel(self, y_index: int | None = None) -> None:
        def is_valid_line(line) -> bool:
            return line >= 0 and line < 5

        self.pedastels.append(Pedastel(self.current_line, y_index))

        directions = (-1, +1)
        direction = random.choice(directions)
        if is_valid_line(self.current_line + direction):
            self.current_line += direction
        else:
            self.current_line -= direction


    def add_batch_pedastels(self, amount: int) -> None:
        for index in range(8-amount, 8):
            self.add_pedastel(index)

    def refresh_objects(self) -> None:
        self.objects = [*self.pedastels, self.player]

    def clean_up(self) -> None:
        to_be_deleted: list[int] = []
        
        for i in range(len(self.pedastels)):
            if self.pedastels[i].rect.top > settings.WINDOWHEIGHT \
            or self.pedastels[i].rect.right < 0 \
            or self.pedastels[i].rect.left > settings.WINDOWWIDTH:
                self.pedastels[i].kill()
                to_be_deleted.append(i)
        
        for i in to_be_deleted:
            del self.pedastels[i]

        self.refresh_objects()

    
    def restart(self) -> None:
        self.current_line = 2

        self.player = Actor(self.play_lines, hooks=self.hooks)
        self.pedastels: list[Pedastel] = []
        self.objects: list[GameObject] = []

        self.build_scene()

        self.move_down = False
        self.move_down_amount = 0
        self.move_down_velocity = 0

        self.score = 0

        # pygame.mixer.music.play(-1)


    # -------- DEBUG ------- #
    def debug_draw(self):
        for i in self.play_lines:
            pygame.draw.rect(self.surface, (255, 255, 255), i.rect, 3)

    def handle_debug_keys(self, key):
        if key == pygame.constants.K_g:
            Pedastel.reset_height()
            self.build_scene()
        elif key == pygame.constants.K_r:
            self.player.debug_reset_position()