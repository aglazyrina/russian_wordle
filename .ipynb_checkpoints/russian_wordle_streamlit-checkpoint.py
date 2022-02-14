import streamlit as st
import pandas as pd
import numpy as np
import random

import streamlit as st

COLOR_DICT = {
    True : 'green',
    False : 'yellow',
    None : 'grey'
}

MATCHING_LETTERS = ['E', 'T', 'Y', 'O', 'P', 'A', 'H', 'K', 'X', 'C', 'B', 'M']
MATCHING_LETTERS_RUSSIAN = ['Е',  'Т', 'У', 'О', 'Р', 'А', 'Н', 'К', 'Х', 'С', 'В', 'М']
RUS_TO_ENG_DICT = dict(zip(MATCHING_LETTERS_RUSSIAN, MATCHING_LETTERS))
ENG_TO_RUS_DICT = dict(zip(MATCHING_LETTERS, MATCHING_LETTERS_RUSSIAN))

def has_transcription_rus(word):
    check_result = min([x in MATCHING_LETTERS_RUSSIAN for x in word.upper()])
    return check_result

def has_transcription_eng(word):
    check_result = min([x in MATCHING_LETTERS for x in word.upper()])
    return check_result

def transcribe_input(user_word):
    russian_word = ''.join([ENG_TO_RUS_DICT.get(x) for x in user_word.upper()])
    return(russian_word)

def get_color_list(user_word, target_word):
    # create a dicitonary 
    target_word_dict = dict(
        zip(
            list(target_word), range(len(target_word))
        )
    )
    match_info  = [target_word_dict.get(letter) for letter in list(user_word)]
    # Transform into True/False form
    color_list = [COLOR_DICT.get(x == match_info.index(x)) if x != None else 'grey' for x in match_info]
    return color_list

def is_valid(user_word):
    # check for 5 unique letters
    valid = True
    if len(set(user_word)) != 5:
        valid = False
    if not has_transcription_eng(user_word):
        valid = False
    return valid

def highlight_green(s, props=''):
    result = np.where(color_grid[s.name] == 'green', props, '')
    return result

def highlight_yellow(s, props=''):
    result = np.where(color_grid[s.name] == 'yellow', props, '')
    return result

def highlight_grey(s, props=''):
    result = np.where(color_grid[s.name] == 'grey', props, '')
    return result

@st.cache
def load_words_list(text_file_name):
    with open(text_file_name) as f:
        contents = f.read()
    words_list = contents.split(' ')
    # Only look at unique letters
    words_list = [x for x in words_list if len(set(x))==5]
    # Adjust to an english keyboard input
    words_list = [x.upper() for x in words_list if has_transcription_rus(x)]
    return words_list

# @st.cache
def pick_a_word(words_list):
    target_word = random.choice(words_list)
    return target_word

st.title('Russian Wordle')

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading word list...')
# Load words.
words_list = load_words_list('words.txt')
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")


# Initialization
if 'target_word' not in st.session_state:
    st.session_state['target_word'] = pick_a_word(words_list)
    
target_word = st.session_state['target_word']
# Create a text element that shows the word of the day.
# word_to_guess = st.text(target_word)

# Initialization
if 'color_grid' not in st.session_state:
    st.session_state['color_grid'] = []

# Initialization
if 'letter_grid' not in st.session_state:
    st.session_state['letter_grid'] = pd.DataFrame()

# Initialization
if 'letter_styler' not in st.session_state:
    st.session_state['letter_styler'] = pd.DataFrame()
    
# color_grid_show = st.dataframe(st.session_state['color_grid'])

# Initialization
if 'iter' not in st.session_state:
    st.session_state['iter'] = 0
    
def update_table(user_word):
    if is_valid(user_word):
        user_word = transcribe_input(user_word)
        word_list = list(user_word)
        color_list = get_color_list(user_word, target_word)
        st.session_state['letter_grid'] = st.session_state['letter_grid'].append([word_list])
        st.session_state['color_grid'] = st.session_state['color_grid'] + [color_list]
        st.session_state['iter'] += 1
    else:
        st.write(user_word)
        st.write('Invalid word')

# Create an input
user_word = st.text_input('Enter your word')
increment = st.button('Submit', on_click=update_table,kwargs=dict(user_word=user_word))

# st.write(st.session_state['color_grid'])
letter_grid = st.session_state['letter_grid']
letter_grid = letter_grid.reset_index(drop = True)
print(letter_grid)
color_grid = pd.DataFrame(st.session_state['color_grid'])
s2 = letter_grid.style
s2.apply(highlight_green, props='color:black;background-color:#2ecc71', axis=0)
s2.apply(highlight_yellow, props='color:black;background-color:#f1c40f', axis=0)
s2.apply(highlight_grey, props='color:black;background-color:#d5dbdb', axis=0)

# st.write(st.session_state['letter_grid'])
st.write(s2)
