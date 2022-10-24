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


with open('DBs/tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tokenizer_from_json(data)


loaded_model = load_model('DBs/best_model.h5')

'''
with open('raw_test_data.json') as f:
    data = json.load(f)
    tedf = pd.read_json(data)
    # testReviewSet, testReviewDesc
'''


def sentence_split(text):
    return kiwi.split_into_sents(text)


def icon_predict(encoded_sentence):
    result = loaded_model.predict(np.asarray(encoded_sentence).reshape(1, len(encoded_sentence)))
    return np.argmax(result)


def review_to_icons(review):
    reviews = []
    kind = []
    split_review = sentence_split(spell_checker.check(review.replace('&', '&amp;').replace('\u0001', '')).checked.replace('&', '&amp;').replace('\u0001', ''))
    for sentence in split_review:
        reviews.append(sentence.text)
        print('문장 :', sentence.text)
        tagged_sentence = komoran.pos(sentence.text)
        tag_word_set = []
        for tag_word in tagged_sentence:
            if tag_word[1][0] == 'J' or tag_word[1][0] == 'I' or tag_word[1][0] == 'S' or tag_word[1][0] == 'E' or tag_word[1][0:2] == 'XS' or tag_word[1][0:2] == 'NA' or tag_word[1][0:2] == 'NV' or tag_word[1][0:2] == 'NF':
                pass
            else:
                tag_word_set.append(tag_word[0]+tag_word[1])
        encoded_review = np.asarray(tokenizer.texts_to_sequences(tag_word_set)).tolist()
        cleaned_review = []
        # encoded_review : 정수 인코딩 결과
        if len(encoded_review) > 0:
            for r in encoded_review:
                if r != []:
                    cleaned_review.append(r)
            # cleaned_review : 토크나이저에 없던 단어들을 배제한 후의 시퀀스
            print(cleaned_review)
            if len(cleaned_review) > 0:
                match icon_predict(cleaned_review):
                    case 0:
                        kind.append(0)  # 교통
                    case 1:
                        kind.append(1)  # 주변
                    case 2:
                        kind.append(2)  # 치안
                    case 3:
                        kind.append(3)  # 주거
            else:
                kind.append(4)  # 분석 불가 - 아무것도 아님
        else:
            kind.append(4)  # 분석 불가 - 아무것도 아님
    return {'reviews': reviews, 'kind': kind}


# d = review_to_icons('집 앞에 강서 초등학교 있고 현대백화점 롯데 아웃렛 다 접근성이 좋음. 고속버스 터미널도 가까우며 앞에 하나병원 뒤에 현대병원 프라임병원 각종 종합병원이 위치해 있어 살기 너무 좋음')
# d = review_to_icons(tedf.testReviewSet[1])
# print(d)
