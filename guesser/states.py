from enum import Enum


class WorkingState(Enum):
    BEFORE_INIT = 0
    INIT = 1
    WAIT_FOR_START = 2
    LOAD_MUSIC = 3
    WAIT_FOR_ANSWER = 4
    WAIT_FOR_NEXT = 5
    FINISH = 6


class GuesserState(Enum):
    INCORRECT = 0
    ONLY_AUTHOR = 1
    CORRECT = 2