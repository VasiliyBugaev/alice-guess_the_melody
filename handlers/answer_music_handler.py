from guesser.guesser import Guesser
from guesser.states import GuesserState, WorkingState
import random

DONT_UNDERSTAND_TEXTS = ['Не поняла, повторите, пожалуйста']
SUCCESSFUL_TEXTS = ['Ура, вы угадали.', 'Настоящие пивные слоны, так держать!',
                    'Верно, хоть я от вас такого и не ожидала.', 'Вот это да! Правильно.']
UNSUCCESSFUL_TEXTS = ['Не верно, попробуйте еще раз, скажите не знаю или попросите повторить песню.',
                      'К сожалению, вы не угадали. Думайте, товарищи, думайте. '
                      'Также вы можете сказать не знаю или повторить.']
PARTIALLY_SUCCESSFUL_TEXTS = ['Вы угадали исполнителя.  Попробуйте угадать песню.']
PASSED_TEXTS = ['К сожалению, вы не угадали, но не расстраивайтесь.', 'Не судьба, повезет в другой раз.',
                'Кожаные мешки, как же так. Опять не угадали.', 'Надо было думать лучше, эх вы.']

ONE_MORE_SONG = ['Еще одну песню?', 'Едем дальше?', 'Хотите еще?', 'Играем?']


def handle(request, guesser: Guesser):
    if request.get('nlu', {}).get('intents', {}).get('fail') is not None:
        text = (random.choice(PASSED_TEXTS) + (f"Это песня {guesser.get_song()}, "
                                                  f"исполнитель {guesser.get_song_writer()} .") +
                random.choice(ONE_MORE_SONG))
        return text, WorkingState.WAIT_FOR_NEXT
    if request.get('nlu', {}).get('intents', {}).get('repeat') is not None:
        return '', WorkingState.REPEAT
    answer = request.get('command', {})
    if answer:
        result = guesser.check_phrase(answer)
        if result == GuesserState.CORRECT:
            text = (random.choice(SUCCESSFUL_TEXTS) + (f"Это песня {guesser.get_song()}, "
                                                      f"исполнитель {guesser.get_song_writer()} .") +
                    random.choice(ONE_MORE_SONG))
            return text, WorkingState.WAIT_FOR_NEXT
        elif result == GuesserState.ONLY_AUTHOR:
            return random.choice(PARTIALLY_SUCCESSFUL_TEXTS), WorkingState.LOAD_MUSIC
        else:
            return random.choice(UNSUCCESSFUL_TEXTS), WorkingState.LOAD_MUSIC
    else:
        return DONT_UNDERSTAND_TEXTS, WorkingState.LOAD_MUSIC
