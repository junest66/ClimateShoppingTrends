from pycaret.classification import *
import pandas as pd
import numpy as np
import copy


def mapper(data):
    city_mapping = {'강원도': 0, '경기도': 1, '경상북도': 2, '부산광역시': 3, '서울특별시': 4, '인천광역시': 5, '전라북도': 6, '제주특별자치도': 7}
    area_mapping = {'가평군': 0, '강남구': 1, '강동구': 2, '강릉시': 3, '강북구': 4, '강서구': 5, '강화군': 6, '경주시': 7, '계양구': 8, '고양시 덕양구': 9, '고양시 일산동구': 10, '고양시 일산서구': 11, '과천시': 12, '관악구': 13, '광명시': 14, '광주시': 15, '광진구': 16, '구로구': 17, '구리시': 18, '군포시': 19, '금정구': 20, '금천구': 21, '기장군': 22, '김포시': 23, '남구': 24, '남동구': 25, '남양주시': 26, '노원구': 27, '도봉구': 28, '동구': 29, '동대문구': 30, '동두천시': 31, '동래구': 32, '동작구': 33, '마포구': 34, '미추홀구': 35, '부산진구': 36, '부천시': 37, '부평구': 38, '북구': 39, '사상구': 40, '사하구': 41, '서구': 42, '서귀포시': 43, '서대문구': 44, '서초구': 45, '성남시 분당구': 46, '성남시 수정구': 47, '성남시 중원구': 48, '성동구': 49, '성북구': 50, '송파구': 51, '수영구': 52, '수원시 권선구': 53, '수원시 영통구': 54, '수원시 장안구': 55, '수원시 팔달구': 56, '시흥시': 57, '안산시 단원구': 58, '안산시 상록구': 59, '안성시': 60, '안양시 동안구': 61, '안양시 만안구': 62, '양주시': 63, '양천구': 64, '양평군': 65, '여주시': 66, '연수구': 67, '연제구': 68, '연천군': 69, '영도구': 70, '영등포구': 71, '오산시': 72, '옹진군': 73, '용산구': 74, '용인시 기흥구': 75, '용인시 수지구': 76, '용인시 처인구': 77, '은평구': 78, '의왕시': 79, '의정부시': 80, '이천시': 81, '전주시 덕진구': 82, '전주시 완산구': 83, '제주시': 84, '종로구': 85, '중구': 86, '중랑구': 87, '파주시': 88, '평택시': 89, '포천시': 90, '하남시': 91, '해운대구': 92, '화성시': 93}
    main_mapping = {'Clear': 0, 'Clouds': 1, 'Drizzle': 2, 'Dust': 3, 'Fog': 4, 'Haze': 5, 'Mist': 6, 'Rain': 7, 'Sand': 8, 'Smoke':9, 'Snow': 10, 'Thunderstorm': 11}
    
    test = copy.deepcopy(data)
    test['city'] = city_mapping[data['city']]
    test['area'] = area_mapping[data['area']]
    test['main'] = main_mapping[data['main']]
    test['amount'] = 2407611.26 
    test['count'] = 74
    
    str_int_fields = ['gender', 'age', 'married', 'child', 'alien']

    for field in str_int_fields:
        if field in test:
            test[field] = int(test[field])

    test_df = pd.DataFrame(test, index=[0])

    return test_df


def catboost(form_data):
    test = mapper(form_data)

    print(test)
    cat = load_model('catboost')
    
    probabilities = cat.predict_proba(test)
    top_3 = np.argsort(probabilities, axis=1)[:, -3:]
    top_3 = np.squeeze(top_3).tolist()
    category_dict = {
        0: "공연",
        1: "관람(내부)",
        2: "관람(외부)",
        3: "기타일반음식",
        4: "레져업소",
        5: "렌터카",
        6: "숙박",
        7: "양식",
        8: "여행/교통",
        9: "연료",
        10: "오락위락시설",
        11: "유통업",
        12: "유흥주점",
        13: "음료/주류",
        14: "일식",
        15: "자동차유지/정비",
        16: "중식",
        17: "취미교양용품",
        18: "카페/디저트",
        19: "한식",
    }

    value = []
    for top in top_3:
        if top in category_dict:
            value.append(category_dict[top])

    return value
