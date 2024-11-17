import enum
import pygame

import settings
from .pedastel import Pedastel
from .game_object import GameObject
from .play_line import PlayLine


class Actor(GameObject):
    PLAY_LINES: tuple[PlayLine] = []
    
    def __init__(self, play_lines: tuple[PlayLine], pos: list[int, int] = None, size: list[int, int] = None, color: tuple[int, int, int] = settings.RED) -> None:
        size = size if size else (30, 30)
        # treta kolona, na sred na kolonata, na sred na igraco (da ne mu e levata strana na sred tuku neogvata sredina)
        pos = (settings.LINE_WIDTH * 3 - settings.LINE_WIDTH / 2 - size[0] / 2, 
                20)
            #    settings.WINDOWHEIGHT - Pedastel.SIZE[1] - Pedastel.MARGIN_Y - size[1])
        
        Actor.PLAY_LINES = play_lines
        self.line_index = 2
        
        self.velocity = [0, 0]
        self.max_speed = 20
        self.direction = [_ActorMoves.INPLACE, _ActorMoves.DOWN]
        
        super().__init__(pos, size, color)

    def handle_mouse(self, mouse_pos: list[int]) -> None:
        pass
    
    # --- Handle Keyboard move --- #
    def handle_keyboard(self, key: pygame.constants) -> None:
        match key:
            case pygame.locals.K_a:
                self.move_left()

            case pygame.constants.K_d:
                self.move_right()

    def move_left(self):
        if self.is_valid_move(_ActorMoves.LEFT):
            self.direction[0] = _ActorMoves.LEFT
            self.line_index -= 1

    def move_right(self):
        if self.is_valid_move(_ActorMoves.RIGHT):
            self.direction[0] = _ActorMoves.RIGHT
            self.line_index += 1

    def is_valid_move(self, move):
        return self.direction[0] == _ActorMoves.INPLACE and not (
            self.line_index <= 0 and move == _ActorMoves.LEFT \
            or self.line_index >= 4 and move == _ActorMoves.RIGHT
        )
    
    # --- Movement --- #
    def update(self, pedastels: tuple[Pedastel]) -> None:
        self.update_direction()
        self.update_position()

        if self.direction[1] == _ActorMoves.DOWN:
            if self.rect.collideobjects(pedastels):
                self.velocity[1] = -self.max_speed

        if self.direction[0] == _ActorMoves.LEFT:
            self.update_velocity((-1, 0))

        if self.direction[0] == _ActorMoves.RIGHT:
            self.update_velocity((1, 0))


    def update_velocity(self, value: tuple[int, int]) -> None:
        # ---- Y ---- #
        if abs(self.velocity[1] + value[1]) < self.max_speed:
            self.velocity[1] += value[1]
        else:
            self.velocity[1] = self.max_speed

        # ---- X ---- #
        if self.direction[0] == _ActorMoves.LEFT \
                and abs(self.velocity[0] + value[0]) < self.max_speed \
                and self.rect.center[0] >= Actor.PLAY_LINES[self.line_index].rect.center[0]:
            self.velocity[0] += value[0]
            
        elif self.direction[0] == _ActorMoves.RIGHT \
                and abs(self.velocity[0] + value[0]) < self.max_speed \
                and self.rect.center[0] <= Actor.PLAY_LINES[self.line_index].rect.center[0]:
            self.velocity[0] += value[0]

        else:
            self.velocity[0] = 0
            self.rect.left = Actor.PLAY_LINES[self.line_index].rect.center[0] - self.rect.size[0] / 2
            self.direction[0] = _ActorMoves.INPLACE

    def update_direction(self):
        if self.velocity[1] < 0:
            self.direction[1] = _ActorMoves.UP
        else:
            self.direction[1] = _ActorMoves.DOWN        

    def update_position(self):
        self.apply_gravity()
        self.rect.top += self.velocity[1]
        self.rect.left += self.velocity[0]

    def apply_gravity(self) -> None:
        self.update_velocity((0, settings.GRAVITY))


    # === DEBUG === #
    def debug_reset_position(self):
        self.rect.topleft = (settings.LINE_WIDTH * 3 - settings.LINE_WIDTH / 2 - self.rect.size[0] / 2, 
                20)



class _ActorMoves(enum.Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"

    INPLACE = "inplace"
    