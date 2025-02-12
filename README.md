# asdf
250110 ~ 250112 intel_AISW

TF-IDF를 이용해서 현재 읽고 있는 위키 문서와 유사한 문서를 추천 해주는 프로그램입니다.



## 목차

- 



## 개요

나무위키 대부분의 문서에는 관련 문서라는 문단에 현재 문서와 연관되어있는 문서의 하이퍼링크가 달려 있습니다.


하지만, 해당 문단은 문서 작성자가 임의로 추가하는 형식이므로 모든 문서에 관련문서 문단이 없는 문서도 있습니다.


 문서를 읽으면서 해당 문서와 비슷한 주제의 글을 읽고 싶을 때, 추천해주는 프로그램이나 문서 안의 문단이 존재 했으면 좋겠다는 생각을 한 적이 있었고,
TF-IDF 실습을 하면서 위의 아쉬웠던 경험을 개선하는 프로그램을 안들 수 있겠다는 기대감을 안고 프로젝트를 진행 했습니다.

실습에 사용할 데이터는 나무위키에서 제공한 가장 최근 덤프 파일(210301, json)을 사용했으며,
약 8.8GB의 파일을 한번에 다루기에는 작업환경 제약이 많아 2%만 추출해서 실습했습니다.


## 디렉토리 구조
```commandline
C:.
├─data
│  ├─raw_data
│  │  └─namuwiki_20210301.json
│  ├─namuwiki_downsize.json
│  └─namuwiki_cleand_data.csv
├─format_files
│  ├─malgum.ttf
│  └─stopwords_kor.csv
├─models
│  ├─tfidf.pickle
│  ├─Tfidf_namuwiki.mtx
│  └─word2vec_namuwiki.model
├─src_img
│  └─image_directory
├─job01_resize_data.py
├─job02_data_preprocessing.py
├─job03_TF-IDF.py
├─job04_word2vec.py
├─job05_recommendation.py
├─job06_ui_recommendation_improve.py
├─job_sub_visualization_for_data_management_model_validation.py
├─job_sub_wordcloud_for_data_management_model_validation.py
├─namu_recommendation.ui
├─README.md
├─requirements.txt
└─model_validation
   ├─job01_1_resize_data_model_validation.py
   ├─job02_1_data_preprocessing_model_validation.py
   ├─job03_1_TF-IDF_model_validation.py
   ├─job04_1_word2vec_model_validation.py
   └─job05_1_recommendation_model_validation.py
```
 


## 작업 프로세스

- 덤프 파일 2%로 다운사이징
- 데이터 전처리
- TF-IDF로 벡터화
- UI로 추천 프로그램 구현


### 덤프 파일 2%로 다운사이징
#### **job01_resize_data.py**

덤프 파일을 바로 사용하기엔 용량이 매우 커서 10%만 추출해서 사용하는 과정

2% 추출 기준은 리스트에서 50의 몫인 번호에 해당하는 행을 추출해서 './data' 디렉토리에 'namuwiki_downsize.json' 파일로 저장합니다.
 
 

추출된 데이터의 행의 수: 16,014 

**주의사항**
해당 코드는 32GB 이상 메모리가 필요합니다!



### 데이터 전처리
#### **job02_data_preprocessing.py**

추출된 json 파일을 pandas, Okt, re, numpy를 이용해서 데이터 전처리를 진행합니다.

- 한글(가 ~ 힣)에 포함된 문장만 남기고 제거합니다.
- Okt로 토큰화를 진행합니다.
- 명사, 동사, 형용사 이외의 토큰은 제거합니다.
- stopword에 포함된 단어와 2글자 미만의 단어, stopword에 포함되지 않은 쓰레기 데이터를 제거합니다.
- 내용이 비어있거나 100토큰 미만의 데이터도 드랍합니다.

100 토큰 미만의 데이터는 의미분석이 안되고 노이즈 데이터가 될 가능성이 높기에 제거했습니다.

데이터의 행의 수: 16,014 => 11,384


### TF-IDF로 벡터화
#### **job03_TF-IDF.py**

토큰화 된 데이터를 벡터화하는 코드

16,014개의 데이터 기준으로 단어 제한 없이 진행했을 때, 토큰의 수는 139,827개로 과하게 많았다.

이후 TF-IDF를 다시 진행 했을 때,
- 문서당 단어 갯수를 2,000개로 제한했다.
- 문서에 5번 이하로 언급되는 단어는 제외한다. => 희귀단어 제거
- 80% 이샹 문서에서 등장한 단어는 제외한다.

#### **job04_word2vec.py**





### UI로 추천 프로그램 구현




## 문제점괴 해결방법

### 1. 작업환경의 메모리 부족
처음에 데이터를 추출할 때, 노트북 환경(16GB 메모리)은 메모리 부족 경고가 뜨면서 데이터 추출을 할 수가 없었다.
```commandline
MemoryError

Process finished with exit code 1
```
**해결 방법**
32GB의 메모리를 가진 컴퓨터에서 추출을 진행하였다.


job01_1_resize_data_lowMEM.py에서 순차적으로 로드해서 작업을 진행하려 했으나, 해당 덤프 파일은 jsonl 형식이 아닌 json 파일이기에,
순차적으로 로드하지 못하고 한번에 로드해야 하기에, 32GB 메모리를 가진 컴퓨터에서 추출을 진행하였다.


### 2. 개요 정보부족




## 라이센스

본 프로젝트에서는 [나무위키 덤프 데이터](https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4%20MDict)를 사용하였습니다.  
해당 데이터는 **CC-BY-NC-SA 2.0 KR 라이선스**에 따라 제공됩니다.

### 데이터 출처 및 라이선스
- **데이터 출처:** [나무위키 MDict 덤프](https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4%20MDict)
- **라이선스:** [CC-BY-NC-SA 2.0 KR](https://creativecommons.org/licenses/by-nc-sa/2.0/kr/)
- **사용 목적:** 비영리 연구 및 학습용

### 라이선스 조건
본 프로젝트는 **비영리적인 목적으로 진행**되었으며, 다음과 같은 조건을 준수합니다:
1. **저작자 표시 (BY):** 데이터를 사용할 때 반드시 출처를 명시해야 합니다.  
2. **비영리 목적 (NC):** 상업적 이용은 금지됩니다.  
3. **동일조건 변경허락 (SA):** 가공된 데이터를 공유할 경우 동일한 라이선스를 적용해야 합니다.  

