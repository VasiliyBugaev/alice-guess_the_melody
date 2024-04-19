from guesser.states import WorkingState
import random


def handle(request):
    if request.get('nlu', {}).get('intents', {}).get('YANDEX.CONFIRM'):
        return WorkingState.WAIT_FOR_START
    elif request.get('nlu', {}).get('intents', {}).get('YANDEX.REJECT'):
        return WorkingState.FINISH
    else:
        return WorkingState.WAIT_FOR_NEXT
