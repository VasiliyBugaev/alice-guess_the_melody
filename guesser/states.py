from enum import Enum


class WorkingState(Enum):
    BEFORE_INIT = 0
    INIT = 1
    WAIT_FOR_START = 2
    REPEAT = 3
    LOAD_MUSIC = 4
    WAIT_FOR_ANSWER = 5
    WAIT_FOR_NEXT = 6
    FINISH = 7


class GuesserState(Enum):
    INCORRECT = 0
    ONLY_AUTHOR = 1
    CORRECT = 2