# 나무위키
#
# 나무위키에서 제공한 가장 최근 덤프 파일을 이용해서 현제 읽고 있는 페이지 기반 연관 페이지 추천 프로그램
# 사용한 Dump 파일은 20210301 버전 - 8.83GB

# 주의! 이 코드는 최소 메모리가 32GB임!

import json

# 변환할 json 파일을 읽어온다.
with open('./data/namuwiki_downsize.json', 'r', encoding='utf-8') as json_file:
    raw_data = json.load(json_file)

# 전체 데이터의 10%저장 => 10의 몫으로 분리
data_chunk = raw_data[:len(raw_data) // 100]            # 86702 => 867

with open('./data/namuwiki_downsize_model_validation.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_chunk, json_file, ensure_ascii=False, indent=4)