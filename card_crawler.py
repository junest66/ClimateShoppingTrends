from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import json

# 상수 정의
BASE_URL = "https://card-gorilla.com/search/card?cate=CRD&search_benefit="
WAIT_TIME = 10
MAX_CARDS = 20


def crawl_and_save_each_category():
    benefit_name_mapping = {
        "retail": "유통업",
        "leisure": "레져업소",
        "fuel": "연료",
        "accommodation": "숙박",
        "auto_maintenance": "자동차유지/정비",
        "restaurant": "음식점",
        "cafe_dessert": "카페/디저트",
        "beverage_liquor": "음료/주류",
        "travel_transport": "여행/교통",
        "recreation": "오락위락시설",
        "hobby_culture": "취미교양용품",
        "observation": "관람",
        "performance": "공연",
        "car_rental": "렌터카",
        "nightclub": "유흥주점",
    }
    base_dir = os.path.join("static", "json")  # static/json 디렉토리 경로 설정
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)  # 디렉토리가 존재하지 않으면 생성

    for english_category_name, korean_category_name in benefit_name_mapping.items():
        cards = fetch_recommended_cards_by_category(korean_category_name)
        file_name = f"{english_category_name}.json"
        file_path = os.path.join(base_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(cards, f, ensure_ascii=False, indent=4)
        print(
            f"Crawled and saved {len(cards)} cards for {english_category_name} in {file_path}"
        )


# 카드추천을 위한 업종분류
def fetch_recommended_cards_by_category(category):
    """
    주어진 업종에 따라 추천 카드를 크롤링합니다.
    """
    print(f"*********************** {category} 관련 추천 카드 ***********************\n")
    benefit_code_mapping = {
        "유통업": [9],
        "레져업소": [8, 70],
        "연료": [21],
        "숙박": [18, 110],
        "자동차유지/정비": [20],
        "음식점": [24],
        "카페/디저트": [22],
        "음료/주류": [24, 134, 22, 127],
        "여행/교통": [5, 18],
        "오락위락시설": [8, 71, 72],
        "취미교양용품": [14, 16, 9],
        "관람": [8, 19, 71, 69],
        "공연": [19, 112],
        "렌터카": [18, 107],
        "유흥주점": [24, 134]
    }
    benefit_codes = benefit_code_mapping.get(category, [])
    return crawl_cards_for_benefits(benefit_codes)


# 업종에 관련된 카드를 크롤링
def crawl_cards_for_benefits(benefit_codes):
    """
    주어진 혜택 코드에 따라 카드 정보를 크롤링합니다.
    """
    driver = webdriver.Chrome()
    base_url = "https://card-gorilla.com/search/card?cate=CRD&search_benefit="
    driver.get(f"{base_url}{','.join(map(str, benefit_codes))}")
    time.sleep(3)

    try:
        # 광고 닫기 버튼을 찾아 클릭
        close_ad_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.q-btn"))
        )
        close_ad_button.click()
    except Exception as e:
        print(f"광고 닫기 버튼 클릭 중 오류 발생: {e}")

    try:
        # "카드 더보기" 버튼을 찾아 클릭
        load_more_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.lst_more"))
        )
        load_more_button.click()
    except Exception as e:
        print(f"카드 더보기 버튼 클릭 중 오류 발생: {e}")

    cards = []  # 최종 카드 정보를 저장할 리스트
    for card_index in range(1, MAX_CARDS + 1):  # 10개 추가된 상태에서 총 20개 카드를 크롤링
        card_info = extract_card_info(driver, card_index)
        if card_info:
            cards.append(card_info)
        else:
            break

    driver.quit()
    return cards


# 광고 닫기
def close_advertisement(driver):
    try:
        close_ad_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.q-btn"))
        )
        close_ad_button.click()
    except Exception as e:
        print(f"광고 닫기 버튼 클릭 중 오류 발생: {e}")


# 카드 더보기
def load_more_cards(driver):
    try:
        load_more_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.lst_more"))
        )
        load_more_button.click()
    except Exception as e:
        print(f"카드 더보기 버튼 클릭 중 오류 발생: {e}")


def extract_card_info(driver, card_index):
    try:
        card_name = get_card_detail(driver, card_index, "span.card_name")
        if not card_name:  # 카드 이름이 없으면 None 반환
            return None

        card_info = {
            "benefits": [],
            "name": card_name,
            "card_company": get_card_detail(driver, card_index, "span.card_corp"),
            "card_img_url": get_card_detail(driver, card_index, "img"),
        }

        for benefit_index in range(1, 4):
            benefit_key = get_card_detail(
                driver, card_index, "i", benefit_index=benefit_index
            )
            benefit_value = get_card_detail(
                driver, card_index, "span", benefit_index=benefit_index
            )
            if benefit_key and benefit_value:
                card_info["benefits"].append(
                    {"key": benefit_key, "value": benefit_value}
                )

        return card_info

    except Exception as e:
        print(f"카드 인덱스 {card_index}에서 세부 정보 추출 중 오류 발생: {e}")
        return None


def get_card_detail(driver, card_index, selector, benefit_index=None):
    """
    주어진 셀렉터를 사용하여 카드의 세부 정보를 가져옵니다.
    """
    try:
        if selector == "img":
            base_selector = f"#q-app > section > div.search_card > section > div > article.con_area > article > ul > li:nth-child({card_index}) > div > div.card_img > p > img"
            return (
                WebDriverWait(driver, 1)
                .until(EC.presence_of_element_located((By.CSS_SELECTOR, base_selector)))
                .get_attribute("src")
            )
        elif selector != "img":
            base_selector = f"#q-app > section > div.search_card > section > div > article.con_area > article > ul > li:nth-child({card_index}) > div > div.card_data > div.name > p > {selector}"

            if benefit_index:
                base_selector = f"#q-app > section > div.search_card > section > div > article.con_area > article > ul > li:nth-child({card_index}) > div > div.card_data > div.sale > p:nth-child({benefit_index}) > {selector}"
            return (
                WebDriverWait(driver, 1)
                .until(EC.presence_of_element_located((By.CSS_SELECTOR, base_selector)))
                .text
            )
    except Exception as e:
        print(f"카드 인덱스 {card_index}에서 세부 정보 추출 중 오류 발생: {e}")
        return None


# 각 업종별로 크롤링 실행 및 JSON 파일 저장
# crawl_and_save_each_category()
