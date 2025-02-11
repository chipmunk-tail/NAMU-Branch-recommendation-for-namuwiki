# 나무위키
#
# TF-IDF 벡터화를 하는 코드
# 작업환경 사양 문제로 토큰 수를 10,000개로 제한
# 문서 내 5번 이하로 등장하는 희귀 단어 제거
# 모든 문서 80%에서 등장한 단어 제거


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle


# 데이터 경로 지정
cleand_csv_path = './data/namuwiki_cleaned_data.csv'
pickle_path = './models/tfidf.pickle'
mtx_path = './models/Tfidf_namuwiki.mtx'


df_namu = pd.read_csv(cleand_csv_path)
df_namu.info()

Tfidf = TfidfVectorizer(
    sublinear_tf=True,
    max_features=10000,   # 가장 중요한 상위 10,000개 단어만 사용 (단어 수 줄이기)
    min_df=5,             # 5개 이하의 문서에 등장한 단어 제거 (희귀 단어 제거)
    max_df=0.8            # 80% 이상의 문서에서 등장한 단어 제거 (너무 자주 등장하는 단어 제거)
)
Tfidf_matrix = Tfidf.fit_transform(df_namu.text)
print(Tfidf_matrix.shape)

with open(pickle_path, 'wb') as f:
    pickle.dump(Tfidf, f)

mmwrite(mtx_path, Tfidf_matrix)