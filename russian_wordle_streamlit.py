import streamlit as st
import pandas as pd
import numpy as np
import random
import streamlit as st
import wordle_toolkit as wt

COLOR_DICT = {
    True : 'green',
    False : 'yellow',
    None : 'grey'
}

def get_color_list(user_word, target_word):
    user_word_list = list(user_word)
    target_word_list = list(target_word)
    all_target_letters = set(target_word_list)
    match_info  = [x[0]==x[1] for x in zip(user_word_list,target_word_list)]
    color_list = []
    for i in range(0,len(user_word_list)):
        if user_word_list[i] in all_target_letters:
            if match_info[i] == True:
                color = 'green'
            else:
                color = 'yellow'
        else:
            color = 'grey'
        color_list.append(color)
    return color_list

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
    # Adjust to an english keyboard input
    words_list = [x.upper() for x in words_list if wt.has_transcription(x)]
    return words_list

def update_table(user_word):
    if wt.is_valid(user_word):
        user_word = wt.transcribe_input(user_word)
        word_list = list(user_word)
        color_list = get_color_list(user_word, target_word)
        st.session_state['letter_grid'] = st.session_state['letter_grid'].append([word_list])
        st.session_state['color_grid'] = st.session_state['color_grid'] + [color_list]
        st.session_state['game_state'] = 'Guesses left: {}'.format(6 - st.session_state['iter'])
        st.session_state['iter'] += 1
        if st.session_state['iter'] == 6:
            st.session_state['game_state'] = 'Game Over'
        elif st.session_state['iter'] > 6:
            st.stop()
    else:
        st.session_state['game_state'] = 'Invalid word: {}'.format(user_word)
    

st.title('Russian Wordle')

# Create a text element and let the user know the data is loading.
data_load_state = st.text('Loading word list...')
# Load words
# TODO: Choose random file from sources
words_list = load_words_list('words.txt')
# Notify the user that the word list was successfully loaded.
data_load_state.text('Loading word list...done!')

# Initialization
if 'target_word' not in st.session_state:
    st.session_state['target_word'] = random.choice(words_list)
# Initialization
if 'game_state' not in st.session_state:
    st.session_state['game_state'] = 'Guesses left: 6'

target_word = st.session_state['target_word']

#Create a text element that shows the word of the day.
#word_to_guess = st.text(target_word)

letter_list = wt.MATCHING_LETTERS

#Create a text element that tells the user if their word is wrong or they lost.
game_state = st.text(st.session_state['game_state'])

# Initialization
if 'color_grid' not in st.session_state:
    st.session_state['color_grid'] = []

# Initialization
if 'letter_grid' not in st.session_state:
    st.session_state['letter_grid'] = pd.DataFrame()

# Initialization
if 'iter' not in st.session_state:
    st.session_state['iter'] = 0

# Create an input
user_word = st.text_input('Enter your word')
submit = st.button('Submit', on_click=update_table,kwargs=dict(user_word=user_word))

letter_grid = st.session_state['letter_grid']
letter_grid = letter_grid.reset_index(drop = True)
print(letter_grid)
print(iter)
color_grid = pd.DataFrame(st.session_state['color_grid'])
s2 = letter_grid.style
s2.apply(highlight_green, props='color:black;background-color:#2ecc71;font-size: 1.5em;', axis=0)
s2.apply(highlight_yellow, props='color:black;background-color:#f1c40f;font-size: 1.5em;', axis=0)
s2.apply(highlight_grey, props='color:black;background-color:#d5dbdb;font-size: 1.5em;', axis=0)
st.write(s2)
