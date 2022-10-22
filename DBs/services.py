import json
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import pandas as pd
import numpy as np
from konlpy.tag import Komoran
from kiwipiepy import Kiwi
from hanspell import spell_checker


kiwi = Kiwi()
komoran = Komoran()


with open('tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tokenizer_from_json(data)


loaded_model = load_model('best_model.h5')


with open('raw_test_data.json') as f:
    data = json.load(f)
    tedf = pd.read_json(data)
    # testReviewSet, testReviewDesc


def sentence_split(text):
    return kiwi.split_into_sents(text)


def icon_predict(encoded_sentence):
    result = loaded_model.predict(np.asarray(encoded_sentence).reshape(1, len(encoded_sentence)))
    print(result)
    print(pd.DataFrame(result))
    return np.argmax(result)


def review_to_icons(review):
    split_review = sentence_split(spell_checker.check(review.replace('&', '&amp;').replace('\u0001', '')).checked.replace('&', '&amp;').replace('\u0001', ''))
    for sentence in split_review:
        tagged_sentence = komoran.pos(sentence.text)
        tag_word_set = []
        for tag_word in tagged_sentence:
            if tag_word[1][0] == 'J' or tag_word[1][0] == 'I' or tag_word[1][0] == 'S' or tag_word[1][0] == 'E' or tag_word[1][0:2] == 'XS' or tag_word[1][0:2] == 'NA' or tag_word[1][0:2] == 'NV' or tag_word[1][0:2] == 'NF':
                pass
            else:
                tag_word_set.append(tag_word[0]+tag_word[1])
        encoded_review = np.asarray(tokenizer.texts_to_sequences(tag_word_set)).tolist()
        cleaned_review = []
        for r in encoded_review:
            if r != []:
                cleaned_review.append(r)
        match icon_predict(cleaned_review):
            case 0:
                print('교통 정보')
                break
            case 1:
                print('주변 정보')
                break
            case 2:
                print('치안 정보')
                break
            case 3:
                print('주거 정보')
                break


review_to_icons(tedf.testReviewSet[1])
