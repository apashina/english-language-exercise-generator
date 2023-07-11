import re
import random

import pandas as pd
import gensim.downloader as api
import spacy
import en_core_web_sm
import contractions


from langdetect import detect
from word_forms.word_forms import get_word_forms

# загрузка предварительно обученной модели с помощью API Gensim Downloader
model = api.load('glove-wiki-gigaword-100')
# a general-purpose model with tagging, parsing, lemmatization and named entity recognition
# малая модель spacy
nlp = spacy.load('en_core_web_sm')

def select_verb_form(row):
    token_list = [token for token in nlp(row['sentence']) if token.pos_ == 'VERB']
    if len(token_list) == 0 or detect(row['sentence']) != 'en':
        return row
    
    try:
        word = random.choice(token_list).text
        response_options = list(get_word_forms(word.lower())['v'])
        if not response_options:
            return row
        response_options = [w for w in response_options if ' not' not in w]
        if word.istitle():
            response_options = [w.title() for w in response_options]
        random.shuffle(response_options)

        row['type'] = 'select_verb_form'
        row['description'] = 'Выберите глагол в правильной форме'
        row['object'] = re.sub(f'\\b{word}\\b', '_____', row['sentence'], count=1)
        row['response_options'] = response_options
        row['right_answer'] = word
    except:
        pass
    return row

def select_auxiliary_verb(row):
    token_list = [token for token in nlp(contractions.fix(row['sentence'])) if token.pos_ == 'AUX']
    if len(token_list) == 0 or detect(row['sentence']) != 'en':
        return row
    
    try:
        word = random.choice(token_list).text
        response_options = list(get_word_forms(word.lower())['v'])
        if not response_options:
            return row
        response_options = [w for w in response_options if not("n't" in w or ' not' in w)]
        
        if word.istitle():
            response_options = [w.title() for w in response_options]
        random.shuffle(response_options)

        row['type'] = 'select_auxiliary_verb'
        row['description'] = 'Выберите вспомогательный глагол'
        obj = re.sub(r'\b(can)(not)\b', r'\1 \2', contractions.fix(row['sentence']), flags=re.IGNORECASE)
        row['object'] = re.sub(f'\\b{word}\\b', '_____', obj, count=1)
        row['response_options'] = response_options
        row['right_answer'] = word
    except:
        pass
    return row

def select_similar_word(row):
    
    token_list = [token for token in nlp(row['sentence']) if token.pos_ in ['NOUN', 'ADV', 'ADJ']]
    if len(token_list) == 0 or detect(row['sentence']) != 'en':
        return row
    
    try:
        word = random.choice(token_list).text
        response_options = [tup[0] for tup in model.similar_by_word(word.lower(), topn=3)] + [word]
        if word.istitle():
            response_options = [w.title() for w in response_options]
        random.shuffle(response_options)

        row['type'] = 'select_word_from_similar_words'
        row['description'] = 'Выберите подходящее по смыслу слово'
        row['object'] = re.sub(f'\\b{word}\\b', '_____', row['sentence'], count=1)
        row['response_options'] = response_options
        row['right_answer'] = word
    except:
        pass
    return row


def fill_missing_aux(row):
    
    token_list = [token for token in nlp(contractions.fix(row['sentence'])) if token.pos_ == 'AUX']
    if len(token_list) == 0 or detect(row['sentence']) != 'en':
        return row
 
    word = random.choice(token_list).text
    
    row['type'] = 'fill_missing_aux'
    row['description'] = 'Впишите пропущенный вспомогательный глагол'
    obj = re.sub(r'\b(can)(not)\b', r'\1 \2', contractions.fix(row['sentence']), flags=re.IGNORECASE)
    row['object'] = re.sub(fr'\b{word}\b', '_____', obj, count=1)
    row['response_options'] = []
    row['right_answer'] = word

    return row


def fill_missing_det(row):
    
    token_list = [token for token in nlp(row['sentence']) if token.tag_ == 'DT']
    if len(token_list) == 0 or detect(row['sentence']) != 'en':
        return row
 
    word = random.choice(token_list).text
    
    row['type'] = 'fill_missing_det'
    row['description'] = 'Впишите пропущенный определитель'
    row['object'] = re.sub(fr'\b{word}\b', '_____', row['sentence'], count=1)
    row['response_options'] = []
    row['right_answer'] = word

    return row


def fill_missing_prp(row):
    
    token_list = [token for token in nlp(row['sentence']) if token.tag_ == 'PRP$']
    if len(token_list) == 0 or detect(row['sentence']) != 'en':
        return row
 
    word = random.choice(token_list).text
    
    row['type'] = 'fill_missing_prp'
    row['description'] = 'Впишите пропущенное притяжательное местоимение'
    row['object'] = re.sub(fr'\b{word}\b', '_____', row['sentence'], count=1)
    row['response_options'] = []
    row['right_answer'] = word

    return row


def determine_type_of_noun_phrases(row):
    chunk_list = [ch for ch in nlp(row['sentence']).noun_chunks if len(ch) > 2]
    if len(chunk_list) < 2 or detect(row['sentence']) != 'en':
        return row
    noun_chunk = random.choice(chunk_list)
    response_options = list({spacy.explain(ch.root.dep_) for ch in nlp(row['sentence']).noun_chunks})
    if len(response_options) < 2:
        return row
    random.shuffle(response_options)
    
    row['type'] = 'base_noun_phrases'
    row['description'] = 'Чем является главное существительное в выделенной фразе'
    row['object'] = re.sub(fr'\b({noun_chunk.text})\b', r'**\1**', row['sentence'])
    row['response_options'] = response_options
    row['right_answer'] = spacy.explain(noun_chunk.root.dep_)
    return row


def restore_order_of_parts_of_speech(row):
    sentence = re.sub('"', '', contractions.fix(row['sentence']))
    token_list = [spacy.explain(token.pos_) for token in nlp(sentence)]
    if len(token_list) < 3 or len(token_list) > 10 or detect(row['sentence']) != 'en':
        return row

    response_options = token_list[:]
    random.shuffle(response_options)
    
    row['type'] = 'part_of_speech'
    row['description'] = 'Восстановите порядок следования частей речи в предложении'
    row['object'] = sentence
    row['response_options'] = response_options
    row['right_answer'] = token_list
    return row


def restore_word_order(row):
    sentence = re.sub('"', '', contractions.fix(row['sentence']))
    token_list = [token.text for token in nlp(sentence)]
    if len(token_list) < 3 or len(token_list) > 9 or detect(row['sentence']) != 'en':
        return row

    response_options = token_list[:]
    random.shuffle(response_options)
    
    row['type'] = 'word_order'
    row['description'] = 'Расставьте слова предложения в правильном порядке'
    row['object'] = ' '
    row['response_options'] = response_options
    row['right_answer'] = token_list
    return row


def select_correct_sentence(row):
    sentence = re.sub('"', '', contractions.fix(row['sentence']))
    sentence = re.sub(r'\b(can)(not)\b', r'\1 \2', sentence, flags=re.IGNORECASE)
    sentence_1, sentence_2 = sentence, sentence

    token_list = [token.text for token in nlp(sentence) if token.pos_ in ['VERB', 'AUX']]
    if len(token_list) == 0 or detect(row['sentence']) != 'en':
        return row
    
    try:
        random.shuffle(token_list)
        word_count = 0
        while word_count < len(token_list) and word_count <= 1:
            words = list(get_word_forms(token_list[word_count].lower())['v'])
            if not words:
                return row
            words = [w for w in words if not("n't" in w or ' not' in w or w == token_list[word_count].lower())]
            if len(words) < 2:
                return row

            if token_list[word_count].istitle():
                words = [w.title() for w in words]
            random.shuffle(words)

            sentence_1 = re.sub(fr'\b{token_list[word_count]}\b', words[0], sentence_1, count=1)
            sentence_2 = re.sub(fr'\b{token_list[word_count]}\b', words[1], sentence_2, count=1)
            word_count += 1

        response_options = [sentence, sentence_1, sentence_2]
        random.shuffle(response_options)
        row['type'] = 'select_sentence'
        row['description'] = 'Выберите верное предложение'
        row['object'] = ' '
        row['response_options'] = response_options
        row['right_answer'] = sentence
    except:
        pass
    return row