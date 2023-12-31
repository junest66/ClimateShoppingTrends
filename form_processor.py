from flask import Flask, request, render_template, session
from flask_session import Session  # 세션 관리를 위한 Flask-Session 확장
from franchisee_crawler import franchises
from utill import translate_to_korean
from utill import map_time_to_number
from utill import fetch_cards_by_industry
from utill import industry_remapping
from utill import get_place_data_by_industry_and_region
from utill import get_weather_img_url
from model_recommend import catboost
from weather_fetcher import get_current_local_weather
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config["SESSION_PERMANENT"] = False  # 세션 지속성 설정
app.config["SESSION_TYPE"] = "filesystem"  # 세션 저장 방식 설정
Session(app)  # 세션 확장 초기화


@app.route("/")
def form():
    # 'form.html' 템플릿을 렌더링합니다.
    return render_template("form.html")


@app.route("/middle", methods=["POST"])
def middle():
    province = request.form.get("currentProvince")
    district = request.form.get("currentDistrict")
    weather_info = get_current_local_weather(province, district)
    current_time = map_time_to_number()
    model_data = {
        "time": current_time,  # 시간
        "city": province,  # 광역시도
        "area": district,  # 시군구
        "gender": request.form.get("gender"),  # 성별
        "age": request.form.get("age"),  # 나이대 그룹
        "married": request.form.get("married"),  # 결혼 여부
        "child": request.form.get("children"),  # 자녀 보유 여부
        "alien": request.form.get("influx"),  # 거주지 일치 여부
        "temp": weather_info.get("temp"),
        "feels_like": weather_info.get("feels_like"),
        "rain_1h": weather_info.get("rain_1h"),
        "snow_1h": weather_info.get("snow_1h"),
        "main": weather_info.get("main_weather"),
    }
    # print(model_data)
    korean_user_info = translate_to_korean(model_data)

    # 데이터를 모델에 전달하고 결과를 받습니다.
    recommended_categories = catboost(model_data)

    # 가맹점 추천용 폼 데이터
    franchise_info = {
        "car": request.form.get("car"),  # 주차여부 필터
        # "household": request.form.get("household"),  # 1인 = 혼밥필터, 1이상 = 가족모임 필터
        # "pet": request.form.get("pet"),  # 애견동반 필터
        # "partner": request.form.get("partner"),  # 목적: 데이트필터
        "preference": request.form.get("general_preference"),  # 정렬 필터
        "ambiance": request.form.get("ambiance_preferences"),  # 분위기 필터
    }
    # 날씨 상태에 따른 이미지 URL 결정
    weather_img_url = get_weather_img_url(weather_info['main_weather'], current_time)

    # 날씨 정보에 이미지 주소 추가
    weather_info['weather_img_url'] = weather_img_url

    # 세션에 데이터 저장
    session["model_data"] = model_data
    session["franchise_info"] = franchise_info
    session["recommended_categories"] = recommended_categories
    session["weather_info"] = weather_info

    # 'middle.html' 템플릿을 렌더링합니다.
    return render_template(
        "middle.html",
        user_info=korean_user_info,
        recommended_categories=recommended_categories,
        weather_info=weather_info
    )


@app.route("/submit", methods=["POST"])
def submit():
    # 세션에서 데이터 검색
    model_data = session.get("model_data", {})
    franchise_info = session.get("franchise_info", {})
    selected_industry = request.form.get("selected_industry")
    weather_info = session.get("weather_info")

    # 사용자 정보를 한글로 변환합니다.
    korean_user_info = translate_to_korean(model_data)

    # place가 먹는 곳 관련이면 franchises_crawler, 그 외는place_crawler를 실행하여 결과를 반환
    def which_crawler_to_use(selected_industry, franchise_info, korean_user_info):
        food_related_industries = ["한식", "양식", "일식", "중식", "카페,디저트", "음식점"]
        remapped_industry = industry_remapping(selected_industry)
        remapped_industry = remapped_industry.replace("/", ",")

        if remapped_industry in food_related_industries:
            place_info = franchises(franchise_info, korean_user_info, remapped_industry)
            return place_info
        else:
            return get_place_data_by_industry_and_region(korean_user_info, selected_industry)


    # 결과 페이지 렌더링
    return render_template(
        "result.html",
        selected_industry=selected_industry,
        user_info=korean_user_info,
        places=which_crawler_to_use(
            selected_industry, franchise_info, korean_user_info
        ),
        cards=fetch_cards_by_industry(selected_industry),
        weather_info=weather_info
    )


if __name__ == "__main__":
    app.run(debug=True)
