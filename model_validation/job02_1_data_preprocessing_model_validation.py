# 나무위키
#
# 축소된 json 파일을 전처리 후 csv 파일로 저장하는 단계
# 해당 json 파일은 "namespace", "title", "text", "contributors" 데이터 컬럼을 포함하고 있음
# 필요한 데이터 컬럼은 "title"과 "text"이니 해당 데이터 컬럼만 추출 후 전처리
# 필요없는 문자, 2글자 미만 단어, 100토큰 미만의 데이터는 제거한다.


import json
import pandas as pd
from konlpy.tag import Okt
import numpy as np
import re

# 데이터 경로 지정
downsize_json_path = '../data/namuwiki_downsize_model_validation.json'
cleand_csv_path = './data/namuwiki_cleand_data_model_validation.csv'
stopword_path = '../format_files/stopwords_kor.csv'

# json 파일 열기
with open(downsize_json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# json 파일로 데이터프레임 생성
df_raw = pd.DataFrame(data)

# 원하는 데이터 컬럼만 추출해서 복사
df = df_raw[['title', 'text']].copy()
print(df.head())
print(df.title[0])
print(df.text[0])


# 데이터 전처리
df_stopwords = pd.read_csv(stopword_path)
stopwords = list(df_stopwords['stopword_kor'])

okt = Okt()
cleand_sentences = []

for txt in df.text:
    # 쓸모없는 문자 변환
    txt = re.sub(r'\n', ' ', txt)
    txt = re.sub(r'\r', ' ', txt)
    txt = re.sub('[^가-힣]', ' ', txt)

    tokened_text = okt.pos(txt, stem=True)
    print(tokened_text)

    df_token = pd.DataFrame(tokened_text, columns=['word', 'class'])
    df_token = df_token[(df_token['class'] == 'Noun') |
                        (df_token['class'] == 'Verb') |
                        (df_token['class'] == 'Adjective')]

    # 되었다 => 되어다 로 변해서 토큰화가 되는 문제 제거
    df_token['word'] = df_token['word'].replace('되어다', '되다')
    print(df_token)

    words = []
    for word in df_token.word:
        if 1 < len(word):
            if word not in stopwords:
                words.append(word)
    cleand_sentence = ' '.join(words)
    cleand_sentences.append(cleand_sentence)
    print(cleand_sentences)


# cleand_sentences를 데이터 프레임에 대입
df.loc[:, 'text'] = cleand_sentences

# 빈 문자열을 NaN으로 변경
df.loc[:, 'text'] = df['text'].replace('', np.nan)
df.loc[:, 'text'] = df['text'].apply(lambda x: np.nan if isinstance(x, str) and x.strip() == '' else x)

# 토큰수가 100개 미만인 데이터는 삭제
df['word_count'] = df['text'].apply(lambda x: len(str(x).split()))
df_filtered = df[df['word_count'] > 100].copy()

df_filtered.dropna(subset=['text'], inplace=True)
df_filtered.drop(columns=['word_count'], inplace=True)

print(f"cleand_sentences 행의 수: {len(cleand_sentences)}")
print(f"df_modify 행의 수: {len(df)}")
print(df.head())

df_filtered.to_csv(cleand_csv_path, index = False)