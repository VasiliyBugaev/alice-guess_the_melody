from random import randint
import random
from guesser import guesser, states
from handlers import start_handler, intro_handler, answer_music_handler, next_handler
from parsers import csv_answer_parser as CSV
from text_worker import checker

current_state = states.WorkingState.BEFORE_INIT
guess_checker = guesser.Guesser()
parser = CSV.CsvAnswerParser()
guess_checker.set_data('MACAN', 'Asphalt 8')


def handler(event, context):
    request = event.get('request', {})
    global current_state

    #set default values for ening session
    end_session = 'false'
    response_body = {}
    if request.get('nlu', {}).get('intents', {}).get('exit') or current_state == states.WorkingState.FINISH:
        text = 'Жаль, но спасибо за игру, кожаные мешки'
        current_state = states.WorkingState.FINISH
        parser.clear_used_songs()
        end_session = 'true'
    elif current_state == states.WorkingState.BEFORE_INIT:
        text, current_state = intro_handler.handle(request)
    elif current_state in [states.WorkingState.INIT, states.WorkingState.WAIT_FOR_START, states.WorkingState.REPEAT]:
        if current_state != states.WorkingState.REPEAT:
            parser.random_data()
        audio = parser.get_audio()
        not_start = current_state != states.WorkingState.INIT
        with_intro = current_state != states.WorkingState.REPEAT
        text, current_state, audio_link = start_handler.handle(request, audio,
                                                               with_text=with_intro,
                                                               dont_check_start=not_start)
        if audio_link:
            response_body['tts'] = audio_link
        song_writer, song = parser.get_answer()
        guess_checker.set_data(song_writer, song)
    elif current_state == states.WorkingState.LOAD_MUSIC:
        text, current_state = answer_music_handler.handle(request, guess_checker)
        if current_state == states.WorkingState.REPEAT:
            return handler(event, context)
    elif current_state == states.WorkingState.WAIT_FOR_NEXT:
        current_state = next_handler.handle(request)
        if current_state == states.WorkingState.WAIT_FOR_NEXT:
            text = 'Я не понимаю, скажите поехали, или хватит'
        else:
            return handler(event, context)
    else:
        text = 'Я не понимаю, скажите поехали, или хватит'

    response_body['end_session'] = end_session
    response_body['text'] = text
    response = {
        'version': event['version'],
        'session': event['session'],
        'response': response_body
    }

    return response


def test_init():
    global current_state
    current_state= states.WorkingState.BEFORE_INIT
    empty_request = {
        "request": {},
        "session": {},
        "version": "1.0",
    }
    response = handler(event=empty_request, context='')
    assert response['response']['text']

def test_load_music():
    global current_state
    current_state = states.WorkingState.INIT
    empty_request = {
        "request": {
            'nlu': {
                'intents': {
                    'start': {},
                },
            },
        },
        "session": {},
        "version": "1.0",
    }
    response = handler(event=empty_request, context='')
    assert response['response']['tts']


def main():
    test_init()
    test_load_music()


if __name__ == "__main__":
    main()
