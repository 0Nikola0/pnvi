import pygame

import settings
from hooks import EventHook
from enums import ActorMoves
from .pedastel import Pedastel
from .play_line import PlayLine
from .game_object import GameObject

class Actor(GameObject):
    PLAY_LINES: tuple[PlayLine] = []
    WENT_UP = 0
    
    def __init__(
            self,
            play_lines: tuple[PlayLine],
            pos: list[int, int] = None,
            size: list[int, int] = None,
            color: tuple[int, int, int] = settings.RED,
            hooks: dict[str, EventHook] = None
        ) -> None:
        # Bese 30, 30, smeniv go koa ja staviv slikata
        size = size if size else (40, 40)
        pos = (settings.LINE_WIDTH * 3 - settings.LINE_WIDTH / 2 - size[0] / 2, 
               Pedastel.BOTTOM_HEIGHT - (Pedastel.SIZE[1] + Pedastel.GAP_Y) - Pedastel.SIZE[1] - Pedastel.MARGIN_Y - size[1])
        
        Actor.PLAY_LINES = play_lines
        self.line_index = 2
        
        self.velocity = [0, 0]
        self.max_speed = 20
        self.direction = [ActorMoves.INPLACE, ActorMoves.DOWN]

        self.x_buffer = None

        self.sprite = pygame.transform.scale(pygame.image.load(
            s if hooks and (sh := hooks.get("skin_hook", None)) and (s := sh.read_data().get("current_skin", None))
            else "assets/characters/player2.png"
        ).convert_alpha(), size)
        self.sound = pygame.mixer.Sound("assets/sounds/player_sound2.mp3")
        self.sound.set_volume(1)

        self.death_sound = pygame.mixer.Sound("assets/sounds/player_death.mp3")
        self.death_sound.set_volume(1)

        super().__init__(pos, size, color)
    
    # --- Handle Keyboard move --- #
    def handle_keyboard(self, key: pygame.constants) -> None:
        match key:
            case pygame.locals.K_a:
                self.move_left()

            case pygame.constants.K_d:
                self.move_right()

    def move_left(self) -> None:
        if self.direction[0] != ActorMoves.INPLACE:
            self.x_buffer = ActorMoves.LEFT
        
        elif self.is_valid_move(ActorMoves.LEFT):
            self.direction[0] = ActorMoves.LEFT
            self.line_index -= 1

    def move_right(self) -> None:
        if self.direction[0] != ActorMoves.INPLACE:
            self.x_buffer = ActorMoves.RIGHT
        
        elif self.is_valid_move(ActorMoves.RIGHT):
            self.direction[0] = ActorMoves.RIGHT
            self.line_index += 1

    def is_valid_move(self, move) -> bool:
        return not (
            self.line_index <= 0 and move == ActorMoves.LEFT \
            or self.line_index >= 4 and move == ActorMoves.RIGHT
        )
    
    # --- Movement --- #
    def update(self, pedastels: tuple[Pedastel]) -> None:
        self.update_direction()
        self.update_position()

        if self.direction[1] == ActorMoves.DOWN:
            if (p := self.rect.collideobjects(pedastels)) and self.rect.centery < p.rect.centery:
                self.velocity[1] = -self.max_speed * 0.65
                Actor.WENT_UP = p.y_index
                # self.sound.play()

        if self.direction[0] == ActorMoves.LEFT:
            self.update_velocity((-1, 0))

        if self.direction[0] == ActorMoves.RIGHT:
            self.update_velocity((1, 0))


    def update_velocity(self, value: tuple[int, int]) -> None:
        # ---- Y ---- #
        if abs(self.velocity[1] + value[1]) < self.max_speed:
            self.velocity[1] += value[1]
        else:
            self.velocity[1] = self.max_speed

        # ---- X ---- #
        if self.direction[0] == ActorMoves.LEFT \
                and abs(self.velocity[0] + value[0]) < self.max_speed \
                and self.rect.center[0] >= Actor.PLAY_LINES[self.line_index].rect.center[0]:
            self.velocity[0] += value[0]
            
        elif self.direction[0] == ActorMoves.RIGHT \
                and abs(self.velocity[0] + value[0]) < self.max_speed \
                and self.rect.center[0] <= Actor.PLAY_LINES[self.line_index].rect.center[0]:
            self.velocity[0] += value[0]

        else:
            self.velocity[0] = 0
            self.rect.left = Actor.PLAY_LINES[self.line_index].rect.center[0] - self.rect.size[0] / 2
            self.direction[0] = ActorMoves.INPLACE

    def update_direction(self) -> None:
        if self.velocity[1] < 0:
            self.direction[1] = ActorMoves.UP
        else:
            self.direction[1] = ActorMoves.DOWN  

        # Ako kliknes levo / desno pred da zastane kockata na podlogata,
        # togaj taj klik ode u buffer
        # tuka se apply-nuva taj buffer
        if self.direction[0] == ActorMoves.INPLACE and self.x_buffer:
            self.direction[0] = self.x_buffer
            self.update_velocity((self.x_buffer.value, 0))
            self.line_index += self.x_buffer.value
            self.x_buffer = None

    def update_position(self) -> None:
        self.apply_gravity()
        self.rect.top += self.velocity[1]
        self.rect.left += self.velocity[0]

    def apply_gravity(self) -> None:
        self.update_velocity((0, settings.GRAVITY))

    def is_dead(self) -> bool:
        return self.rect.top > settings.WINDOWHEIGHT

    def draw(self, surface):
        surface.blit(self.sprite, self.rect)

    # === DEBUG === #
    def debug_reset_position(self) -> None:
        self.rect.topleft = (settings.LINE_WIDTH * 3 - settings.LINE_WIDTH / 2 - self.rect.size[0] / 2, 
                20)
