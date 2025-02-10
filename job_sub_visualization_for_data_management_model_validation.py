#
#
#


import pandas as pd
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
from matplotlib import font_manager, rc
import matplotlib as mpl
import os

# CPU 코어 갯수 지정
os.environ["LOKY_MAX_CPU_COUNT"] = "4"  # 사용 가능한 CPU 개수로 조정


font_path = './format_files/malgun.ttf'
font_name = font_manager.FontProperties(fname = font_path).get_name()
mpl.rcParams['axes.unicode_minus'] = False
rc('font', family = font_name)

embedding_model = Word2Vec.load('./models/word2vec_namuwiki_model_validation.model')
key_word = '응급의료정보센터'
# sim_word = embedding_model.wv.most_similar(key_word, topn = 10)
# print(sim_word)

if key_word in list(embedding_model.wv.index_to_key):
    sim_word = embedding_model.wv.most_similar(key_word, topn=10)
    print(sim_word)
else:
    print("해당 단어는 없습니다.")


# 시각화
vectors = []
labels = []
for label, _ in sim_word:
    labels.append(label)
    vectors.append(embedding_model.wv[label])
print(vectors[0])
print(len(vectors[0]))

df_vectors = pd.DataFrame(vectors)
print(df_vectors.head())

tsne_model = TSNE(perplexity=9, n_components=2, init='pca', n_iter=2500)
new_value = tsne_model.fit_transform(df_vectors)
df_xy = pd.DataFrame({'words':labels, 'x':new_value[:, 0], 'y':new_value[:, 1]})
df_xy.loc[df_xy.shape[0]] = (key_word, 0, 0)
print(df_xy)
print(df_xy.shape)

plt.figure(figsize=(8, 8))
plt.scatter(0, 0, s=1500, marker='*')

for i in range(len(df_xy)):
    a = df_xy.loc[[i, 10]]
    plt.plot(a.x, a.y, '-D', linewidth=1)
    plt.annotate(df_xy.words[i], xytext=(1, 1), xy=(df_xy.x[i], df_xy.y[i]),
                 textcoords='offset points', ha='right', va='bottom')
plt.show()