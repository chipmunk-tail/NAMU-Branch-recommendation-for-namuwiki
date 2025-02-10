# 나무위키
#
# 나무위키에서 제공한 가장 최근 덤프 파일을 이용해서 현제 읽고 있는 페이지 기반 연관 페이지 추천 프로그램
# 사용한 Dump 파일은 20210301 버전 - 8.83GB

# 해당 코드는 메모리가 부족한 작업환경을 위해 한번에 한줄씩 스트림, 한번에 한줄씩 읽어오는 방식이다.
# 16GB RAM 노트북의 경우는 약 8분, 커밋은 47GB

import json

# 파일을 저장할 경로
input_path = "./data/raw_data/namuwiki_20210301.json"
output_path = "./data/namuwiki_downsize.json"

# 줄 단위로 읽어서 10%만 저장
with open(input_path, "r", encoding="utf-8") as f_in, open(output_path, "w", encoding="utf-8") as f_out:
    selected_lines = []
    for i, line in enumerate(f_in):
        if i % 10 == 0:  # 전체 데이터의 10%만 선택
            selected_lines.append(json.loads(line))

    json.dump(selected_lines, f_out, ensure_ascii=False, indent=4)
