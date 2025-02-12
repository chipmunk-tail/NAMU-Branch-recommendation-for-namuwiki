import pandas as pd
import numpy as np
import re
import json

# 파일 경로
cleand_csv_path = './data/namuwiki_cleaned_data_filtered.csv'  # 전처리된 CSV 파일 경로
original_json_path = './data/namuwiki_downsize_2P.json'  # 오리지널 JSON 파일 경로
output_csv_path = './data/namuwiki_cleaned_data_filtered_overview.csv'  # 생성할 새로운 CSV 파일 경로

# 전처리된 CSV 파일 읽기
df_preprocessed = pd.read_csv(cleand_csv_path)

# 오리지널 JSON 파일 읽기
with open(original_json_path, 'r', encoding='utf-8') as f:
    original_data = json.load(f)


# 'title'을 기준으로 text 데이터를 추가하는 함수
def get_text_from_json(title, json_data):
    title = title.strip()  # 공백 제거
    for item in json_data:
        if isinstance(item, dict) and item.get("title") == title:
            return item.get("text", np.nan)  # 'text'가 없으면 빈 문자열 반환
    return np.nan  # 찾을 수 없으면 빈 값을 반환


# 전처리된 CSV의 각 'title'에 해당하는 'text'를 찾아 새로운 컬럼 추가
# 'namuwiki_cleaned_data_filtered.csv'에 있는 title만 처리
df_preprocessed['text'] = df_preprocessed['title'].apply(lambda title: get_text_from_json(title, original_data))

# 개요 추출 및 전처리
overview = []

for title, txt in zip(df_preprocessed['title'], df_preprocessed['text']):
    # 'namuwiki_cleaned_data_filtered.csv'에 존재하는 title만 처리
    if isinstance(txt, str) and '== 개요 ==' in txt:  # 개요가 있는지 확인
        str_start = txt.find('== 개요 ==') + 8
        str_end = txt.find('==', str_start)

        if str_end == -1:  # == 개요 == 이후에 == 가 없다면 끝까지 자르기
            txt = txt[str_start:]
        else:
            txt = txt[str_start: str_end]

        txt = re.sub(r'\[\[파일:[^\]]*\]\]', '', txt)  # 이미지 태그 제거
        txt = re.sub(r'\[\[([^\|]+)\|[^\]]*\]\]', r'\1', txt)  # 내부 링크에서 텍스트만 추출
        txt = re.sub(r'==[^\n]*==', '', txt)  # '== 개요 ==' 등의 마크업 제거
        txt = re.sub(r'[^\w\s]', '', txt)  # 특수문자나 불필요한 기호 제거
        overview.append(txt.strip())  # 앞뒤 공백 제거
    else:
        overview.append("개요가 없습니다.")  # 개요가 없으면 '개요가 없습니다.'

# 'text' 컬럼을 'overview'로 덮어쓰기
df_preprocessed['text'] = overview

# 새로운 CSV 파일로 저장
df_preprocessed.to_csv(output_csv_path, index=False)

print(f"새로운 CSV 파일이 생성되었습니다: {output_csv_path}")
