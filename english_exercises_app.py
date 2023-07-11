import re

import streamlit as st
import pandas as pd
from random import randint
from sentence_splitter import SentenceSplitter
from english_exercises import (select_verb_form,
                               select_auxiliary_verb,
                               select_similar_word,
                               fill_missing_aux,
                               fill_missing_det,
                               fill_missing_prp,
                               determine_type_of_noun_phrases,
                               restore_order_of_parts_of_speech,
                               restore_word_order,
                               select_correct_sentence)


st.markdown('<h1 style="text-align:center; color:red">Генератор упражнений по английскому языку</h1>', 
            unsafe_allow_html=True)
st.markdown('##### Вставьте текст для создания упражнений')

if 'text_entered' not in st.session_state:
    st.session_state.text_entered = False

def fill_in_text_area():
    st.session_state.text_entered = True
    st.session_state.clicked = False

text = st.text_area('Если это поле останется пустым, будет использован текст **"Little Red-Cap"** by Grimm Brothers', 
                    on_change=fill_in_text_area)
'---'
def create_df(text):
    splitter = SentenceSplitter(language='en')
    sentences = splitter.split(text=text)
    sentences = list(filter(lambda x: x, sentences))
    df = pd.DataFrame(columns=['sentence', 'type', 'description', 'object', 'response_options', 'right_answer'])
    df['sentence'] = sentences
    df_1 = df.copy().apply(select_verb_form, axis=1).dropna().reset_index(drop=True)
    df_2 = df.copy().apply(select_auxiliary_verb, axis=1).dropna().reset_index(drop=True)
    df_3 = df.copy().apply(select_similar_word, axis=1).dropna().reset_index(drop=True)
    df_4 = df.copy().apply(fill_missing_aux, axis=1).dropna().reset_index(drop=True)
    df_5 = df.copy().apply(fill_missing_det, axis=1).dropna().reset_index(drop=True)
    df_6 = df.copy().apply(fill_missing_prp, axis=1).dropna().reset_index(drop=True)
    df_7 = df.copy().apply(determine_type_of_noun_phrases, axis=1).dropna().reset_index(drop=True)
    df_8 = df.copy().apply(restore_order_of_parts_of_speech, axis=1).dropna().reset_index(drop=True)
    df_9 = df.copy().apply(restore_word_order, axis=1).dropna().reset_index(drop=True)
    df_10 = df.copy().apply(select_correct_sentence, axis=1).dropna().reset_index(drop=True)
    return pd.concat([df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8, df_9, df_10], ignore_index=True)

if st.session_state.text_entered:
    if re.sub(r'[ \n\t]', '', text):
        st.session_state.data = create_df(text)
        st.session_state.text_entered = False
    else:
        st.session_state.data = pd.read_json('data_js.json')
        st.session_state.text_entered = False

if 'data' not in st.session_state:
    st.session_state.data = pd.read_json('data_js.json')

st.markdown('<p style="color:red">В боковом меню выберите тип и количество упражнений</p>', 
            unsafe_allow_html=True)

# словарь названий упражнений
td = st.session_state.data.loc[~st.session_state.data[['type', 'description']].duplicated(), ['description', 'type']].copy()
exercise_names = dict(zip(td.description, td.type))
exercise_types = list(exercise_names.keys())

if 'rand_state' not in st.session_state:
    st.session_state.rand_state = randint(1, 1000)

def change_type_or_number():
    st.session_state.clicked = False
    st.session_state.rand_state += 1

type_exercise = st.sidebar.selectbox(
    '**Выберите тип упражнения**',
    options=exercise_types,
    on_change=change_type_or_number
)

type_exercise = exercise_names[type_exercise]

number_exercises = st.sidebar.slider(
    '**Установите количество упражнений**',
    min_value=0, 
    max_value=st.session_state.data.query('type == @type_exercise').shape[0], 
    value=1,
    step=1,
    on_change=change_type_or_number
)


if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

start_generating = st.button('**Сгенерировать упражнения**', type='primary', on_click=click_button)

def check_solution_1(answer, right_answer, result):
    if not answer:
        pass
    elif answer == right_answer:
        st.success('Верно!', icon="🎉")
        result += 1
    else:
        st.error('Неверно!', icon="🚨")
    return result

def check_solution_2(answer, right_answer, result):
    if answer == '–––––':
        pass
    elif answer == right_answer:
        st.success('Верно!', icon="🎉")
        result += 1
    else:
        st.error('Неверно!', icon="🚨")
    return result


if st.session_state.clicked:
    data_1 = (st.session_state.data
              .query('type == @type_exercise')
              .sample(number_exercises, random_state=st.session_state.rand_state)
              .copy()
              .reset_index(drop=True))
    result = 0
    for index, row in data_1.iterrows():        
        st.markdown('#### Упражнение # ' + str(index + 1))
        st.write(f"{row['description']}:")

        if row['type'] in ['part_of_speech', 'word_order']:
            st.write(row['object'])
            answer = st.multiselect('nolabel',
                                    row['response_options'],
                                    label_visibility="hidden",
                                    key=f'multi{index}')
            result = check_solution_1(answer, row['right_answer'], result)
            '---'
        elif row['type'] == 'select_sentence':
            st.write(row['object'])
            answer = st.selectbox('nolabel',
                                    ['–––––'] + row['response_options'],
                                    label_visibility="hidden",
                                    key=f'selbox{index}')
            result = check_solution_2(answer, row['right_answer'], result)
            '---'
        else:
            col1, col2 = st.columns(2)

            with col1:
                st.write('')
                st.write(row['object'])

            if row['response_options']:       
                with col2:
                    answer = st.selectbox('nolabel',
                                            ['–––––'] + row['response_options'],
                                            label_visibility="hidden",
                                            key=f'box{index}')
                    result = check_solution_2(answer, row['right_answer'], result)
                '---'
            else:
                with col2:
                    answer = st.text_input('nolabel',
                                            label_visibility="hidden",
                                            key=f't_input{index}',
                                            placeholder='Введите текст')
                    result = check_solution_1(answer, row['right_answer'], result)
                '---'

    if result == number_exercises:
        st.success('Отлично!')
        st.balloons()
    else:
        st.error('Не все упражнения выполнены правильно!')