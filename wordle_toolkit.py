import pymorphy2
import nltk

MATCHING_LETTERS = ['E', 'T', 'Y', 'O', 'P', 'A', 'H', 'K', 'X', 'C', 'B', 'M']
MATCHING_LETTERS_RUSSIAN = ['Е',  'Т', 'У', 'О', 'Р', 'А', 'Н', 'К', 'Х', 'С', 'В', 'М']

ENG_TO_RUS_DICT = dict(zip(MATCHING_LETTERS, MATCHING_LETTERS_RUSSIAN))
ENG_TO_RUS_DICT.update(dict(zip(MATCHING_LETTERS_RUSSIAN, MATCHING_LETTERS_RUSSIAN)))

morph = pymorphy2.MorphAnalyzer()

def has_transcription(word):
    in_russian = min([x in MATCHING_LETTERS_RUSSIAN for x in word.upper()])
    in_english = min([x in MATCHING_LETTERS for x in word.upper()])
    check_result = max(in_russian, in_english)
    return check_result

def transcribe_input(user_word):
    russian_word = ''.join([ENG_TO_RUS_DICT.get(x) for x in user_word.upper()])
    return(russian_word)

def is_valid(word):
    valid = True
    # check for 5 letters
    if len(word) != 5:
        valid = False
    # check for transcription
    if not has_transcription(word):
        valid = False
    return valid



