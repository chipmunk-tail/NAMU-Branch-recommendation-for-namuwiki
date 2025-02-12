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

# 데이터 경로 지정
ui_path = './namu_recommendation.ui'
mtx_path = './models/Tfidf_namuwiki_cleaned_data_filtered.mtx'
pickle_path = './models/tfidf_cleaned_data_filtered.pickle'
model_path = './models/word2vec_namuwiki_cleaned_data_filtered.model'
cleand_csv_path = './data/namuwiki_cleaned_data_filtered.csv'
overview_path = './data/namuwiki_cleaned_data_filtered_overview.csv'

from_window = uic.loadUiType(ui_path)[0]

class Exam(QWidget, from_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.Tfidf_matrix = mmread(mtx_path).tocsr()
        with open(pickle_path, 'rb') as f:
            self.Tfidf = pickle.load(f)
        print("Loading Word2Vec model...")
        self.embedding_model = Word2Vec.load(model_path)
        print("Word2Vec model loaded successfully!")

        self.df_namu = pd.read_csv(cleand_csv_path)
        self.df_overview = pd.read_csv(overview_path)
        self.titles = list(self.df_namu.title)
        self.titles.sort()
        self.cb_title.addItem("")               # combo box 첫번째 선택창을 빈 칸으로 세팅
        for title in self.titles:
            self.cb_title.addItem(title)
        self.cb_title.setCurrentIndex(0)        # combo box 첫 번째 선택

        # 자동완성 코드
        model = QStringListModel()
        model.setStringList(self.titles)
        completer = QCompleter()
        completer.setModel(model)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setFilterMode(Qt.MatchContains)  # 입력한 단어가 포함된 모든 항목을 보여줌

        completer.activated[str].connect(self.on_completer_activated)  # 자동완성 선택 후 처리

        self.le_keyword.setCompleter(completer)

        # 기존 시그널 연결
        self.cb_title.currentIndexChanged.connect(self.combobox_slot)
        self.btn_recommend.clicked.connect(self.btn_slot)
        self.le_keyword.returnPressed.connect(self.btn_slot)


    def initUI(self):
        self.setWindowTitle("NAMU-Branch 나무위키 문서 자동 추천 프로그램")

        self.default_text = "여기에 입력하세요"  # 기본 텍스트
        self.le_keyword.setText(self.default_text)

        # 포커스 이벤트 핸들러 연결
        self.le_keyword.focusInEvent = self.on_focus_in
        self.le_keyword.focusOutEvent = self.on_focus_out


    def on_focus_in(self, event):
        """ 입력창이 클릭되었을 때 기본 텍스트 삭제 """
        if self.le_keyword.text() == self.default_text:
            self.le_keyword.clear()  # 텍스트 삭제
        super().focusInEvent(event)

    def on_focus_out(self, event):
        """ 입력창에서 벗어날 때 비어있으면 기본 텍스트 복원 """
        if self.le_keyword.text().strip() == "":
            self.le_keyword.setText(self.default_text)
        super().focusOutEvent(event)

    def btn_slot(self):
        keyword = self.le_keyword.text()
        if keyword in self.titles:
            recommendation = self.recommendation_by_title(keyword)
        else:
            recommendation = self.recommendation_by_keyword(keyword)

        if recommendation:
            self.lbl_recommendation.setText(recommendation)
            overview = self.getOverview(keyword)
            self.lb_overview.setText(overview)



    def combobox_slot(self):
        title = self.cb_title.currentText()
        print(title)
        recommendation = self.recommendation_by_title(title)
        self.lbl_recommendation.setText(recommendation)
        overview = self.getOverview(title)
        self.lb_overview.setText(overview)


    def recommendation_by_title(self, tlt):
        namu_idx = self.df_namu[self.df_namu.title == tlt].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[namu_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        recommendation = '\n'.join(list(recommendation))
        return recommendation

    def recommendation_by_keyword(self, keyword):
        try:
            sim_word = self.embedding_model.wv.most_similar(keyword, topn=10)
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
        sentence_vec = self.Tfidf.transform([sentence])
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

    def on_completer_activated(self, text):
        # 자동완성에서 선택된 텍스트를 받아서 처리
        self.le_keyword.setText(text)
        self.btn_slot()  # 자동완성 선택 후 바로 추천 처리

    def getOverview(self, keyword):
        target_data = self.df_overview[self.df_overview['title'] == keyword].index.tolist()
        if not target_data:
            return "개요를 찾을 수 없습니다."
        target_data_num = target_data[0]
        overview = self.df_overview.iloc[target_data_num, 1]

        self.lb_overview.setText(overview)
        self.lb_overview.setWordWrap(True)
        return overview


if __name__ == '__main__':
    # 노트북 윈도우 배열 문제
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)     # PyQt가 Windows 배율 설정을 감지하고 조절하도록 함
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)        # 아이콘, 그래픽 요소가 흐려지는 문제 해결

    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())
