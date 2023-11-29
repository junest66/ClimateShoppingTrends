import json
import os
import requests


# 위도 경도를 찾는 함수
def get_coords(province, city_district):
    file_path = os.path.join(
        os.path.dirname(__file__), "static", "json", "regions_coordinates.json"
    )
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    search_name = f"{province} {city_district}"
    for item in data:
        if item["name"] == search_name:
            return item["lat"], item["lon"]
    raise ValueError(f"{province} {city_district}에 대한 위도 경도를 찾을 수 없음")


# 날씨 정보를 가져오는 함수
def get_weather(lat, lon):
    api_key = "f008c6fef5d45c810a55681a43c6c267"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    return response.json()


# 지역명을 받아 날씨 정보를 반환하는 함수
def get_current_local_weather(province, city_district):
    lat, lon = get_coords(province, city_district)
    weather_data = get_weather(lat, lon)
    return {
        "temp": weather_data.get("main", {}).get("temp"),
        "feels_like": weather_data.get("main", {}).get("feels_like"),
        "rain_1h": weather_data.get("rain", {}).get("1h", 0),
        "snow_1h": weather_data.get("snow", {}).get("1h", 0),
        "main_weather": weather_data.get("weather", [{}])[0].get("main"),
    }
