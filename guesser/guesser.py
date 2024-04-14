from text_worker import checker
from .states import GuesserState


class Guesser:
    __song_writer__: str = None
    __song__: str = None

    def set_data(self, song_writer: str, song: str):
        self.__song_writer__ = song_writer
        self.__song__ = song

    def check_phrase(self, phrase: str) -> GuesserState:
        if self.__song__ is None or self.__song_writer__ is None:
            return GuesserState.INCORRECT

        if checker.check_answer(phrase, self.__song__):
            return GuesserState.CORRECT
        elif checker.check_answer(phrase, self.__song_writer__):
            return GuesserState.ONLY_AUTHOR
        else:
            return GuesserState.INCORRECT

    def get_song(self):
        return self.__song__

    def get_song_writer(self):
        return self.__song_writer__