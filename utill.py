from datetime import datetime
import os
import json
import csv


# selected_indusrty를 크롤링을 위한 업종으로 재매핑하는 함수
def industry_remapping(selected_industry):
    # 업종 매핑을 위한 사전 정의
    industry_mapping = {
        "연료": "주유",
        "숙박": "숙박",
        "중식": "중식",
        "한식": "한식",
        "일식": "일식",
        "양식": "양식",
        "카페/디저트": "카페,디저트",
        "공연": "공연",
        "렌터카": "렌터카",
        "유흥주점": "유흥주점",
        "레져업소": "레져",
        "자동차유지/정비": "자동차정비",
        "기타일반음식": "음식점",
        "관람(내부)": "관람",
        "관람(외부)": "관람",
        "유통업": "마트",
        "음료/주류": "바",
        "여행/교통": "버스터미널",
        "오락위락시설": "오락",
        "취미교양용품": "문구",
    }

    # 매핑된 값 찾기, 없을 경우 None 반환
    remapped_industry = industry_mapping.get(selected_industry)

    # 매핑된 값이 없는 경우 에러 발생
    if remapped_industry is None:
        raise ValueError(f"업종명 매핑이 존재하지 않음: {selected_industry}")

    return remapped_industry


# form에서 받은 데이터를 한국어로 변환하는 함수
def translate_to_korean(data_list):
    korean_data = {
        "age": {
            "1": "20대이하",
            "2": "20대",
            "3": "30대",
            "4": "40대",
            "5": "50대",
            "6": "60대",
            "7": "70대",
        },
        "gender": {"1": "남성", "2": "여성"},
        "alien": {"1": "거주", "0": "유입"},
        "married": {"1": "기혼", "0": "미혼"},
        "child": {"1": "자녀 있음", "0": "자녀 없음"},
    }

    korean_user_info = {}

    for key, value in data_list.items():
        if key in korean_data:
            korean_user_info[key] = korean_data[key].get(value, value)
        else:
            korean_user_info[key] = value

    return korean_user_info


# 현재 시간을 숫자로 매핑하는 함수
def map_time_to_number():
    current_hour = datetime.now().hour

    # 시간 범위에 따라 숫자 매핑
    if 0 <= current_hour < 6:
        return 1
    elif 6 <= current_hour < 8:
        return 2
    elif 8 <= current_hour < 10:
        return 3
    elif 10 <= current_hour < 12:
        return 4
    elif 12 <= current_hour < 14:
        return 5
    elif 14 <= current_hour < 16:
        return 6
    elif 16 <= current_hour < 18:
        return 7
    elif 18 <= current_hour < 20:
        return 8
    elif 20 <= current_hour < 22:
        return 9
    elif 22 <= current_hour < 24:
        return 10


def fetch_cards_by_industry(industry):
    """
    주어진 업종명(industry)에 해당하는 카드 정보를 JSON 파일에서 읽어 반환합니다.
    """
    industry_name_mapping = {
        "유통업": "retail",
        "레져업소": "leisure",
        "연료": "fuel",
        "숙박": "accommodation",
        "자동차유지/정비": "auto_maintenance",
        "중식": "restaurant",
        "한식": "restaurant",
        "일식": "restaurant",
        "양식": "restaurant",
        "기타일반음식": "restaurant",
        "카페/디저트": "cafe_dessert",
        "음료/주류": "beverage_liquor",
        "여행/교통": "travel_transport",
        "오락위락시설": "recreation",
        "취미교양용품": "hobby_culture",
        "관람(외부)": "observation",
        "관람(내부)": "observation",
        "공연": "performance",
        "렌터카": "car_rental",
        "유흥주점": "nightclub",
    }

    english_industry_name = industry_name_mapping.get(industry, None)
    if not english_industry_name:
        raise ValueError(f"업종명 매핑이 존재하지 않음: {industry}")

    file_path = os.path.join(
        os.path.dirname(__file__), "static", "json", f"{english_industry_name}.json"
    )
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"파일이 존재하지 않음: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        cards = json.load(file)
        return cards


def get_place_data_by_industry_and_region(korean_user_info, industry):
    file_path = os.path.join(os.path.dirname(__file__), "static", "csv", "place_data.csv")
    # 딕셔너리 초기화
    data_list = []
    region = korean_user_info["city"] + " " + korean_user_info["area"]
    # 업종 변환
    if industry in ["관람(내부)", "관람(외부)"]:
        industry = "관람"

    # CSV 파일 읽기
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            row_industry = row['industry']
            row_region = row['region']
            name = row['name']
            category = row['category']
            address = row['address']
            img_url = row['img_url']
            grade = row['grade']

            # 인자로 받은 업종과 지역에 맞는 데이터인 경우 리스트에 추가
            if row_industry == industry and row_region == region:
                data_list.append({
                    'name': name,
                    'category': category,
                    'address': address,
                    'img_url': img_url,
                    'grade': grade
                })

    return data_list