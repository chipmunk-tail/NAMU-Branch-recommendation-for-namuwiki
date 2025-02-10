

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import Qt


from_window = uic.loadUiType('./namu_recommendation.ui')[0]


class Exam(QWidget, from_window):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Tfidf_matrix = mmread('./models/Tfidf_namuwiki_model_validation.mtx').tocsr()
        with open('./models/tfidf_model_validation.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        print("Loading Word2Vec model...")
        self.embedding_model = Word2Vec.load('./models/word2vec_namuwiki_model_validation.model')
        print("Word2Vec model loaded successfully!")


        self.df_namu = pd.read_csv('./data/namuwiki_cleaned_data_model_validation.csv')
        self.titles = list(self.df_namu.title)
        self.titles.sort()
        # self.cb_title.addItem('Test01')
        for title in self.titles:
            self.cb_title.addItem(title)

        # 자동완성 코드
        model = QStringListModel()
        model.setStringList(self.titles)
        completer = QCompleter()
        completer.setModel(model)
        self.le_keyword.setCompleter(completer)


        self.cb_title.currentIndexChanged.connect(self.combobox_slot)
        self.btn_recommend.clicked.connect(self.btn_slot)


    def btn_slot(self):
        keyword = self.le_keyword.text()
        if keyword in self.titles:
            recommendation = self.recommendation_by_title(keyword)
        else:
            recommendation = self.recommendation_by_keyword(keyword)

        # recommendation = self.recommendation_by_keyword(keyword)
        if recommendation:
            self.lbl_recommendation.setText(recommendation)


    def combobox_slot(self):
        title = self.cb_title.currentText()
        print(title)
        recommendation = self.recommendation_by_title(title)
        self.lbl_recommendation.setText(recommendation)


    def recommendation_by_title(self, tlt):
        namu_idx = self.df_namu[self.df_namu.title == tlt].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[namu_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        recommendation = '\n'.join(list(recommendation))
        return recommendation

    def recommendation_by_keyword(self, keyword):
        try:
            sim_word = self.embedding_model.wv.most_similar(keyword, topn = 10)
        except:
            self.lbl_recommendation.setText("제가 모르는 단어에요.")
            return 0
        words = [keyword]
        for word, _ in sim_word:
            words.append(word)
        print(words)
        sentence = []
        count = 10
        for word in words:
            sentence = sentence + [word] * count
            count -= 1
        sentence = ' '.join(sentence)
        sentence_vec  = self.Tfidf.transform([sentence])
        cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        recommendation = '\n'.join(list(recommendation))
        return recommendation


    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:11]
        wikiIdx = [i[0] for i in simScore]
        recmovieList = self.df_namu.iloc[wikiIdx, 0]
        return recmovieList[1:11]


if __name__ == '__main__':

    # 노트북 윈도우 배열 문제
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)     # PyQt가 Windows 배율 설정을 감지하고 조절하도록 함
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)        # 아이콘, 그래픽 요소가 흐려지는 문제 해결

    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())