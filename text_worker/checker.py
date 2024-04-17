from functools import partial
from langdetect import detect, DetectorFactory
from num2words import num2words
from translate import Translator
from transliterate import translit

CORRECTNESS_COEF = 0.5
TRANSLATOR = Translator(to_lang="ru")
DetectorFactory.seed = 66


def is_english_word(text):
    return detect(text) == 'en'


def is_russian_word(text):
    return detect(text) == 'ru'


def is_in_english_characters(text):
    return text.isascii()


def is_similar(word_from_phrase: str, word_from_answer: str) -> bool:
    # print('is digit', word_from_answer.isdigit())
    # print('is in eng', is_in_eng(word_from_answer))
    # print('is is_in_eng2', is_in_eng(word_from_phrase))

    #check if answer word is digit
    if word_from_answer.isdigit():
        if word_from_phrase.isdigit():
            return word_from_phrase == word_from_answer
        else:
            is_ru_digit = num2words(int(word_from_answer), lang='ru') == word_from_phrase
            is_en_digit = num2words(int(word_from_answer), lang='en') == word_from_phrase
            return is_ru_digit or is_en_digit
    #check if answer word is english
    elif is_in_english_characters(word_from_answer):
        if is_in_english_characters(word_from_phrase):
            return word_from_phrase in word_from_answer
        else:
            check_russian_transliteration = word_from_phrase in translit(word_from_answer, 'ru')
            need_translation = is_english_word(word_from_answer)
            check_russian_translation = word_from_phrase in TRANSLATOR.translate(word_from_answer) if need_translation \
                else False
            print(TRANSLATOR.translate(word_from_answer), translit(word_from_answer, 'ru'), word_from_answer, word_from_phrase)
            return check_russian_transliteration or check_russian_translation
    #else answer in russian so check pronounce
    else:
        return word_from_phrase in word_from_answer


def get_words_from_phrase(phrase: str):
    return list(map(lambda word: word.lower(), phrase.split(' ')))


def check_word(answers: list[str], word: str) -> bool:
    for answer in answers:
        if is_similar(word, answer):
            return True
    return False


def check_answer(player_phrase: str, answer: str) -> bool:
    words_in_phrase = get_words_from_phrase(player_phrase)
    words_in_answer = get_words_from_phrase(answer)
    if len(words_in_phrase) < len(words_in_answer):
        return False
    check_word_in_answer = partial(check_word, words_in_answer)
    check_result = list(filter(check_word_in_answer, words_in_phrase))
    print(check_result)
    return len(check_result) >= CORRECTNESS_COEF * len(words_in_answer)
