from datetime import datetime


# form에서 받은 데이터를 한국어로 변환하는 함수
def translate_to_korean(data_list):
    korean_data = {
        "age": {
            "1": "20이하",
            "2": "20대",
            "3": "30대",
            "4": "40대",
            "5": "50대",
            "6": "60대",
            "7": "70대",
        },
        "gender": {"1": "남성", "2": "여성"},
        "influx": {"1": "거주", "0": "유입"},
        "married": {"1": "기혼", "0": "미혼"},
        "children": {"1": "자녀 있음", "0": "자녀 없음"},
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
