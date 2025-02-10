#
#
# downsizing 된 json 파일을 불려들어 전처리 후 csv 파일로 저장하는 단계
# 해당 json 파일은 "namespace", "title", "text", "contributors" 데이터 컬럼을 포함하고 있음
# 필요한 데이터 컬럼은 "title"과 "text"이니 해당 데이터 컬럼만 추출
#

import json
import pandas as pd
from konlpy.tag import Okt
import numpy as np
import re

# 데이터 위치
data_path = './data/namuwiki_downsize_model_validation.json'
clean_data_path = './data/namuwiki_cleand_data_model_validation.csv'

# json 파일 열기
with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# json 파일로 데이터프레임 생성
df_raw = pd.DataFrame(data)

# 원하는 데이터 컬럼만 추출해서 복사
df = df_raw[['title', 'text']].copy()
print(df.head())
print(df.title[0])
print(df.text[0])


# 데이터 전처리
df_stopwords = pd.read_csv('./format_files/stopwords_kor.csv')
stopwords = list(df_stopwords['stopword_kor'])

okt = Okt()
cleand_sentences = []

for txt in df.text:

    # 개행문자 제거
    txt = re.sub(r'\n', ' ', txt)
    txt = re.sub(r'\r', ' ', txt)
    txt = re.sub('[^가-힣]', ' ', txt)

    # start_idx = txt.find("== 개요 ==")               # 개요를 찾는다
    # if start_idx == -1:                             # 개요가 없다면
    #     cleand_sentences.append(np.nan)             # nan값을 넣는다.
    #     continue
    # else:
    #     end_idx = txt.find("==", (start_idx + 8))  # 개요 끝부분을 찾는다. 두번째 매개변수는 start 지점
    #     txt = txt[start_idx: end_idx]
    #
    #     txt = re.sub('[^가-힣]', ' ', txt)
    # print(txt)

    tokened_text = okt.pos(txt, stem=True)
    print(tokened_text)

    df_token = pd.DataFrame(tokened_text, columns=['word', 'class'])
    df_token = df_token[(df_token['class'] == 'Noun') |
                        (df_token['class'] == 'Verb') |
                        (df_token['class'] == 'Adjective')]
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



# df.text = cleand_sentences

# df.loc[:, 'text'] = cleand_sentences
# df['text'].replace('', np.nan, inplace=True)  # 빈 문자열을 NaN으로 변경
# df.dropna(inplace = True)

df.loc[:, 'text'] = cleand_sentences
df.loc[:, 'text'] = df['text'].replace('', np.nan)  # 빈 문자열을 NaN으로 변경
df.loc[:, 'text'] = df['text'].apply(lambda x: np.nan if isinstance(x, str) and x.strip() == '' else x)
df.dropna(subset=['text'], inplace=True)

print(f"cleand_sentences 행의 수: {len(cleand_sentences)}")
print(f"df_modify 행의 수: {len(df)}")
print(df.head())

df.to_csv('./data/namuwiki_cleaned_data_model_validation.csv', index = False)


# 867 => 582
