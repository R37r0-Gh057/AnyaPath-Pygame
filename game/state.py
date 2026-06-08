from enum import Enum, auto


class GameState(Enum):
    SPLASH = auto()
    INTRO = auto()
    WORD_LENGTH = auto()
    MATRIX_SELECTION = auto()

    TRANSPOSE_INTRO = auto()
    TRANSPOSE_SELECTION = auto()

    REVEAL = auto()
    PLAY_AGAIN = auto()
    EXIT = auto()