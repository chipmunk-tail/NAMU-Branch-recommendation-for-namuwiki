# 나무위키
#
# 10% 추출된 데이터를 더 작게 추출하는 코드
# 10%의 1% => 원본 데이터의 0.1%
# 10% : 86702 => 0.1% : 867


import json

# 데이터 경로 지정
original_json_path = './data/namuwiki_downsize.json'
downsize_json_path = './data/namuwiki_downsize_model_validation.json'

# 변환할 json 파일을 읽어온다.
with open(original_json_path, 'r', encoding='utf-8') as json_file:
    raw_data = json.load(json_file)

# 전체 데이터의 10%저장 => 10의 몫으로 분리
data_chunk = raw_data[:len(raw_data) // 100]            # 86702 => 867

with open(downsize_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(data_chunk, json_file, ensure_ascii=False, indent=4)