# 나무위키
#
# 워드 클라우드를 확인용


import pandas as pd
from matplotlib.pyplot import figure
from wordcloud import WordCloud
import collections
import matplotlib.pyplot as plt
from matplotlib import font_manager


target_word = 'KBS순천'

# 데이터 경로 지정
font_path = './format_files/malgun.ttf'
cleand_csv_path = './data/namuwiki_cleaned_data_model_validation.csv'


font_name = font_manager.FontProperties(fname = font_path).get_name()
plt.rc('font', family = 'NanumBrunGothic')

df = pd.read_csv(cleand_csv_path)

# 특정 데이터 (예: "title" 열에서 '버스'라는 값이 있는 행)
target_data = df[df['title'] == target_word].index.tolist()
target_data_num = target_data[0]

print(f"특정 데이터 행 수: {target_data_num}")

words = df.iloc[target_data_num, 1].split()
print(df.iloc[target_data_num, 0])

worddict = collections.Counter(words)
worddict = dict(worddict)
print(worddict)                                 # 해당 단어가 몇번 나오는지 딕셔너리 형태로 출력

wordcloud_img = WordCloud(
    background_color = 'white', font_path = font_path).generate_from_frequencies(worddict)
plt.figure(figsize=(12, 12))  # figure 크기 조정
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')  # 축을 제거합니다.
plt.show()