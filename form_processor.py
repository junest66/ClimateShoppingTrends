from flask import Flask, request, render_template
from franchisee_crawler import franchises
from utill import translate_to_korean
from utill import map_time_to_number
from utill import fetch_cards_by_industry
from model_recommend import my_model
from place_crawler import place_other_than_franchises

app = Flask(__name__)


@app.route("/")
def form():
    # 'form.html' 템플릿을 렌더링합니다.
    return render_template("form.html")


@app.route("/submit", methods=["POST"])
def submit():
    model_data = {
        "apr_tizn_c": map_time_to_number(),  # 시간
        "province": request.form.get("currentProvince"),  # 광역시도
        "district": request.form.get("currentDistrict"),  # 시군구
        "gender": request.form.get("gender"),  # 성별
        "age": request.form.get("age"),  # 나이대 그룹
        "married": request.form.get("married"),  # 결혼 여부
        "children": request.form.get("children"),  # 자녀 보유 여부
        "influx": request.form.get("influx"),  # 거주지 일치 여부
    }

    # 데이터를 모델에 전달하고 결과를 받습니다.
    industry = my_model(model_data)

    # 가맹점 추천용 폼 데이터
    franchise_info = {
        "car": request.form.get("car"),  # 주차여부 필터
        # "household": request.form.get("household"),  # 1인 = 혼밥필터, 1이상 = 가족모임 필터
        # "pet": request.form.get("pet"),  # 애견동반 필터
        # "partner": request.form.get("partner"),  # 목적: 데이트필터
        "preference": request.form.get("general_preference"),  # 정렬 필터
        "ambiance": request.form.get("ambiance_preferences"),  # 분위기 필터
    }

    # 사용자 정보를 한글로 변환합니다.
    korean_user_info = translate_to_korean(model_data)

    # place가 먹는 곳 관련이면 franchises_crawler, 그 외는place_crawler를 실행하여 결과를 반환
    def which_crawler_to_use(industry, franchise_info, korean_user_info):
        food_related_industries = ["한식", "양식", "일식", "중식", "카페/디저트"]

        if industry in food_related_industries:
            place_info = franchises(franchise_info, korean_user_info, industry)
        else:
            place_info = place_other_than_franchises(korean_user_info, industry)
        return place_info

    # 결과 페이지 렌더링
    return render_template(
        "result.html",
        industry=industry,
        user_info=korean_user_info,
        place=which_crawler_to_use(industry),
        cards=fetch_cards_by_industry(industry),
    )


if __name__ == "__main__":
    app.run(debug=True)
