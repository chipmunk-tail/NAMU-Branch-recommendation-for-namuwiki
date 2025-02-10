# 나무위키
#
#
#


import json

# JSON 파일을 읽어오기
with open('.data/raw_data/namuwiki_20210301.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# 1/10로 나누어 저장 (전체 데이터의 10%)
data_chunk = data[:len(data) // 10]

with open('./data/namuwiki_resize.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_chunk, json_file, ensure_ascii=False, indent=4)