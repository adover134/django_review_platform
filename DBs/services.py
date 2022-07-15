import sys
from kiwipiepy import Kiwi


def review_to_icon(sentence):
    lines = sentence_spliter(sentence)
    print(lines)
    lines = sentence_encoder(lines)


def sentence_spliter(sentence):
    kiwi = Kiwi()
    lines = []
    tmp = kiwi.split_into_sents(sentence)
    for line in tmp:
        lines.append(line.text)
    return lines


def sentence_encoder(lines):
    return 2


sentences = """
안녕하세요.
냉장고가 없지만 에어컨은 있네요
방이 많이 습해요
건물 입구에 가까워요
"""
'''
sentences = sentence_spliter(sentences)
kiwi = Kiwi()
for sentence in sentences:
    sentence = kiwi.tokenize(sentence)
    for token in sentence:
        if token.tag == 'JKS' or token.tag == 'JKC' or token.tag == 'JKG' or token.tag == 'JKO' or token.tag == 'JKB' or token.tag == 'JKV' or token.tag == 'JKQ' or token.tag == 'JX' or token.tag == 'JC':
            sentence.remove(token)
    print(sentence)
'''