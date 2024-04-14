from guesser.states import WorkingState
import random

INTRO_TEXTS = ['Привет, мои любимые (а может и нет) кожаные друзья. '
               'Сегодня вам выпала уникальная возможность угадать топовые песни. '
               'Чтобы начать играть скажите "Поехали".'
               ' Вперед, работяги! За Родину, отечество и пивных слонов!',

               'Ура, кожаные мешки опять вернулись. Зададим жаришку. '
               'Чтобы начать играть скажите "Поехали". Вперед, работяги! '
               'За Родину, отечество и пивных слонов!',

               'Дорогие друзья, я рада приветствовать вас на интеллектуальном шоу, '
               'где нужно угадывать топовые песни, с целью побороться за ровно ноль рублей ноль копеек. '
               'Чтобы начать играть скажите "Поехали". Вперед, уважаемые!']


def handle(request):
    return random.choice(INTRO_TEXTS), WorkingState.INIT