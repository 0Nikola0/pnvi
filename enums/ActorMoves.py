import enum


class ActorMoves(enum.Enum):
    LEFT = -1
    RIGHT = 1
    UP = "up"
    DOWN = "down"
    INPLACE = "inplace"
