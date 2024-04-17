from guesser.states import WorkingState
import random

NEXT_TRACK_TEXTS = ['Еще одну песню?', 'Едем дальше?', 'Хотите еще?', 'Играем?']


def handle(request):
    if request.get('nlu', {}).get('intents', {}).get('YANDEX.CONFIRM'):
        return random.choice(NEXT_TRACK_TEXTS), WorkingState.WAIT_FOR_START
    elif request.get('nlu', {}).get('intents', {}).get('YANDEX.REJECT'):
        return 'Жаль, но спасибо за игру, кожаные мешки', WorkingState.FINISH
