import settings
from .game_object import GameObject


class Pedastel(GameObject):
    MARGIN_X, MARGIN_Y = 10, 10
    GAP_Y = 50
    SIZE = (settings.LINE_WIDTH - MARGIN_X * 2, 15)
    CURRENT_HEIGHT = settings.WINDOWHEIGHT
    
    def __init__(self, index: int, color: tuple[int, int, int] = settings.GREEN) -> None:
        pos = (index * settings.LINE_WIDTH + Pedastel.MARGIN_X, 
               Pedastel.CURRENT_HEIGHT - Pedastel.SIZE[1] - Pedastel.MARGIN_Y)
        
        super().__init__(pos, Pedastel.SIZE, color)

        Pedastel.CURRENT_HEIGHT -= Pedastel.SIZE[1] + Pedastel.GAP_Y


    @classmethod
    def reset_height(cls):
        cls.CURRENT_HEIGHT = settings.WINDOWHEIGHT