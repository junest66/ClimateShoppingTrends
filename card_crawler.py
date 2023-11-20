from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time


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

    cards = []  # 최종 카드 정보를 저장할 리스트
    for card_index in range(1, 4):
        card_info = extract_card_info(driver, card_index)  # 개별 카드 정보를 저장할 딕셔너리
        if card_info:
            cards.append(card_info)

    driver.quit()
    return cards


def extract_card_info(driver, card_index):
    """
    드라이버와 카드 인덱스를 사용하여 개별 카드 정보를 추출합니다.
    """
    card_info = {"benefits": []}
    card_info["name"] = get_card_detail(driver, card_index, "span.card_name")
    card_info["card_company"] = get_card_detail(driver, card_index, "span.card_corp")
    card_info["card_img_url"] = get_card_detail(driver, card_index, "img")

    for benefit_index in range(1, 4):
        benefit_key = get_card_detail(
            driver, card_index, "i", benefit_index=benefit_index
        )
        benefit_value = get_card_detail(
            driver, card_index, "span", benefit_index=benefit_index
        )
        if benefit_key and benefit_value:
            card_info["benefits"].append({"key": benefit_key, "value": benefit_value})

    return card_info


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
        print(f"세부 정보 추출 중 오류 발생: {e}")
        return None
