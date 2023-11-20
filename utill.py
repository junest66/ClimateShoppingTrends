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