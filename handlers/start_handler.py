from guesser.states import WorkingState
import random

SUCCESSFUL_TEXTS = ['Начинаем игру.', 'Да начнется великая Игра.', 'Ура, погнали.']
UNSUCCESSFUL_TEXTS = ['Я не понимаю, скажите поехали, или хватит']
LOAD_MUSIC_TEXTS = ['Запускаю песню.', 'Подготавливаем трек.', 'Сейчас отожжем.']
FINISH_MUSIC_TEXTS = ['Что же это за удивительная песня?', 'Справитесь с этой песней?',
                      'Тик-так ребята, называйте песенку.', 'Я очень жду вашего ответа.']

SKILL_LINK = '3183b7fb-6d22-4855-9634-0f62b563f859'


def handle(request, song_link, with_text=True, dont_check_start=False):
    if request.get('nlu', {}).get('intents', {}).get('start') is not None or dont_check_start:
        start_text = random.choice(SUCCESSFUL_TEXTS) + random.choice(LOAD_MUSIC_TEXTS) if with_text else ''
        finish_text = random.choice(FINISH_MUSIC_TEXTS)
        audio_link = (start_text + "<speaker audio='dialogs-upload/" + SKILL_LINK + "/" + song_link +
                      ".opus'>" + finish_text)
        return start_text + finish_text, WorkingState.LOAD_MUSIC, audio_link
    else:
        return random.choice(UNSUCCESSFUL_TEXTS), WorkingState.INIT, None
