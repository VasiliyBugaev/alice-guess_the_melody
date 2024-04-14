from random import randint
import random
from guesser import guesser, states
from handlers import start_handler, intro_handler, answer_music_handler
from text_worker import checker

current_state = states.WorkingState.BEFORE_INIT
guess_checker = guesser.Guesser()
guess_checker.set_data('MACAN', 'Asphalt 8')

def handler(event, context):
    translate_state = event.get('state', {}).get('session', {}).get('translate', {})
    last_phrase = event.get('state', {}).get('session', {}).get('last_phrase')
    request = event.get('request', {})
    intents = request.get('nlu', {}).get('intents', {})
    command = request.get('command')

    global current_state

    #set default values for ening session
    end_session = 'false'
    response_body = {
        'end_session': end_session
    }

    if current_state == states.WorkingState.BEFORE_INIT:
        text, current_state = intro_handler.handle(request)
    elif current_state == states.WorkingState.INIT:
        text, current_state, audio_link, author, song = start_handler.handle(request)
        response_body['tts'] = audio_link
        guess_checker.set_data(author, song)
    elif current_state == states.WorkingState.LOAD_MUSIC:
        text, current_state = answer_music_handler.handle(request, guess_checker)
    elif current_state == states.WorkingState.WAIT_FOR_NEXT:

    # elif intents.get('exit'):
    #     text = 'Приятно было попереводить для вас! ' \
    #            'Чтобы вернуться в навык, скажите "Запусти навык Крот-Полиглот". До свидания!'
    #     end_session = 'true'
    # # elif intents.get('help'):
    # #     text = INTRO_TEXT
    # elif intents.get('repeat'):
    #     if last_phrase:
    #         text = last_phrase
    #     else:
    #         text = 'Ох, я забыл, что нужно повторить. Попросите меня лучше что-нибудь перевести.'
    # # elif translate_full:
    # #     text, translate_state = do_translate(translate_full, translate_state, token=token)
    # elif command:
    #     text = 'Не понял вас. Чтобы выйти из навыка "Крот-Полиглот", скажите "Хватит".'

    response_body['text'] = text
    response = {
        'version': event['version'],
        'session': event['session'],
        'response': response_body,
        'session_state': {'translate': translate_state, 'last_phrase': text}
    }

    return response


def main():
    handler({}, {})
    # new_guesser = guesser.Guesser()
    # new_guesser.set_data('MACAN', 'Asphalt 8')
    # guessed = new_guesser.check_phrase('МАКАН')
    #
    # if guessed == states.GuesserState.CORRECT:
    #     result = 'совпадает'
    # elif guessed == states.GuesserState.ONLY_AUTHOR:
    #     result = 'совпадает автор'
    # else:
    #     result = 'не совпадает'
    # print(result)


if __name__ == "__main__":
    main()
