import streamlit as st
import pandas as pd
import numpy as np
import random
import os
import streamlit as st
from translate import Translator
import wordle_toolkit as wt

COLOR_DICT = {
    True : 'green',
    False : 'yellow',
    None : 'grey'
}

HEX_DICT = {
    'green' : '#2ecc71',
    'yellow' : '#f1c40f',
    'grey' : '#d5dbdb',
    'lightgrey' : '#f2f2f2'
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
        for i in range(0,len(user_word)):
            letter = word_list[i]
            new_color = color_list[i]
            old_color = st.session_state['letter_colors'].get(letter)
            if (new_color == 'grey' and old_color !='#f2f2f2') \
            or (new_color == 'yellow' and old_color !='green') or new_color == 'green':
                    st.session_state['letter_colors'].update({letter:new_color})
        st.session_state['letter_grid'] = st.session_state['letter_grid'].append([word_list])
        st.session_state['color_grid'] = st.session_state['color_grid'] + [color_list]
        st.session_state['iter'] += 1
        st.session_state['game_state'] = 'Guesses left: {}'.format(6 - st.session_state['iter'])
        if st.session_state['iter'] == 6:
            st.session_state['game_state'] = 'Game Over'
        elif st.session_state['iter'] > 6:
            st.stop()
    else:
        st.session_state['game_state'] = 'Invalid word: {}'.format(user_word)

def get_letter_html(letter, color):
    hex_color = HEX_DICT.get(color)
    if color == 'lightgrey':
        letter_color = 'black'
    else:
        letter_color = '#f2f2f2'
    output = '<span style="textalign:center;background-color:{};color:{}"> {} </span>'.format(
        hex_color, 'black', letter
    )
    return output

st.title('Russian Wordle')

# Create a text element and let the user know the data is loading.
data_load_state = st.text('Loading word list...')
# Load words
# Choose random file from sources
sources = ['sources/{}'.format(x) for x in os.listdir('sources') if '.txt' in x]
source = random.choice(sources)
source_name = source.split('/')[1].split('.')[0]
source_name_formatted = ' '.join(
    [word.capitalize() for word in source_name.split('_') if word.lower() != 'wordlized']
)
words_list = load_words_list(source)
# Notify the user that the word list was successfully loaded.
data_load_state.text('Loading word list...done!')
source_text = st.text('This word is from "{}"'.format(source_name_formatted))

letter_list = wt.MATCHING_LETTERS_RUSSIAN
# Initialization
if 'target_word' not in st.session_state:
    st.session_state['target_word'] = random.choice(words_list)
if 'game_state' not in st.session_state:
    st.session_state['game_state'] = 'Guesses left: 6'
if 'color_grid' not in st.session_state:
    st.session_state['color_grid'] = []
if 'letter_grid' not in st.session_state:
    st.session_state['letter_grid'] = pd.DataFrame()
if 'letter_colors' not in st.session_state:
    st.session_state['letter_colors'] = dict(zip(letter_list, ['lightgrey' for letter in letter_list]))
if 'iter' not in st.session_state:
    st.session_state['iter'] = 0

target_word = st.session_state['target_word']

#Create a text element that shows the word of the day.
translator= Translator(from_lang="russian",to_lang="english")
translation = translator.translate(target_word)
#word_to_guess = st.text(target_word)
word_to_guess = st.text('This word means "{}" in English'.format(translation))


#Create a text element that tells the user if their word is wrong or they lost.
game_state = st.text(st.session_state['game_state'])

letters_unused = (pd.DataFrame([letter_list], columns = None))

letters_string = ''.join([get_letter_html(letter,color) for (letter,color) in st.session_state['letter_colors'].items()])
st.write('<h3>{}<h3>'.format(letters_string), unsafe_allow_html= True)

# Create an input
user_word = 'place'
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
