# 나무위키
#
#
#


import pandas as pd
from gensim.models import Word2Vec

# 데이터 경로 지정
cleand_csv_path = '../data/namuwiki_cleaned_data_model_validation.csv'
model_path = '../models/word2vec_namuwiki_model_validation.model'

df_namu = pd.read_csv(cleand_csv_path)
df_namu.info()


text = list(df_namu.text)
print(text[0])
tokens = []

for sentence in text:
    token = sentence.split()
    tokens.append(token)
print(tokens[0])

embedding_model = Word2Vec(tokens, vector_size = 200, window = 4,
                           min_count = 20, workers = 4, epochs = 100, sg = 1)   # 벡터 사이즈, 윈도우, 최소문장, CPU코어
embedding_model.save(model_path)
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))