#
#
#


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle


df_namu = pd.read_csv('./data/namuwiki_cleaned_data.csv')
df_namu.info()

Tfidf = TfidfVectorizer(sublinear_tf= True)
Tfidf_matrix = Tfidf.fit_transform(df_namu.text)
print(Tfidf_matrix.shape)

with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)

mmwrite('./models/Tfidf_namuwiki.mtx', Tfidf_matrix)