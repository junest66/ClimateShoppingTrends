from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
import time
import re
import csv
import json
import os


def save_to_csv(data, filename):
    file_exists = os.path.isfile(filename)
    with open(
        filename, mode="a" if file_exists else "w", newline="", encoding="utf-8-sig"
    ) as file:
        fieldnames = [
            "industry",
            "region",
            "name",
            "category",
            "address",
            "img_url",
            "grade",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for row in data:
            writer.writerow(row)


def init_driver():
    """
    웹 드라이버 초기화 및 옵션 설정
    """

    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    # ChromeDriver 자동 설치 및 Service 객체 생성
    service = Service(chromedriver_autoinstaller.install())

    # WebDriver 객체 생성
    return webdriver.Chrome(service=service, options=chrome_options)


def load_search_results(driver, location, category):
    """
    주어진 위치와 카테고리로 네이버 플레이스 검색 결과 페이지 로드
    """
    search_url = f"https://map.naver.com/p/search/{location} {category}"
    driver.get(search_url)
    time.sleep(3)  # 페이지 로딩 대기


# 장소의 목록의 수 가져오기
def find_number_of_li_elements(driver):
    # iframe 전환
    search_iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="searchIframe"]'))
    )
    driver.switch_to.frame(search_iframe)

    # ul을 찾고 li개수 구하기
    ul_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#_pcmap_list_scroll_container > ul")
        )
    )
    # ul 태그 내의 모든 li 태그를 찾기
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")

    # li 태그의 수 계산
    number_of_li_elements = len(li_elements)
    # print("li 태그의 수:", number_of_li_elements)

    return number_of_li_elements


def get_image_url(driver, timeout=10):
    """
    지정된 시간 동안 웹 요소를 기다리고, 해당 요소에서 이미지 URL을 추출합니다.
    """
    css_selector = ".K0PDV, .K0PDV._div"  # 대상 요소의 CSS 선택자

    try:
        # WebDriverWait를 사용하여 이미지 요소 대기
        image_element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )

        # 이미지 스타일 속성에서 URL 추출
        image_style = image_element.get_attribute("style")
        match = re.search(r"url\((.*?)\)", image_style)
        return match.group(1).strip("'\"") if match else None

    except Exception as e:
        print(f"이미지를 찾을 수 없습니다: ", e)
        return None


def get_place_info(driver, index):
    """
    주어진 인덱스에 해당하는 장소 정보 추출
    """
    # 장소 클릭
    try:
        # _pcmap_list_scroll_container > ul > li:nth-child(1) > div.abKxh > a > div.eOFsy > div
        restaurant_selector = (
            f"#_pcmap_list_scroll_container > ul > li:nth-child("
            + str(index)
            + ") > div.qbGlu > div.ouxiq > a:nth-child(1) > div"
        )
        restaurant_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, restaurant_selector))
        )
        driver.execute_script("arguments[0].scrollIntoView();", restaurant_element)
        time.sleep(2)  # 필요에 따라 적절한 대기 시간을 설정할 수 있습니다.
        restaurant_element.click()
    except Exception as e:
        print(f"인덱스 {index}의 요소를 찾을 수 없습니다: ", e)
        return None

    time.sleep(1)

    driver.switch_to.parent_frame()
    # 상세 정보 프레임으로 전환
    entry_iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="entryIframe"]'))
    )
    driver.switch_to.frame(entry_iframe)

    # 장소 이름, 유형, 주소 추출
    name = (
        WebDriverWait(driver, 2)
        .until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#_title > span.Fc1rA"))
        )
        .text
    )

    category = (
        WebDriverWait(driver, 2)
        .until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#_title > span.DJJvD"))
        )
        .text
    )

    # address = (
    #     WebDriverWait(driver, 2)
    #     .until(
    #         EC.presence_of_element_located(
    #             (
    #                 By.CSS_SELECTOR,
    #                 "#app-root > div > div > div > div:nth-child(5) > div > div:nth-child(2) > div.place_section_content > div > div.O8qbU.tQY7D > div > a > span.LDgIH",
    #             )
    #         )
    #     )
    #     .text
    # )

    # 주소를 찾을 선택자들의 리스트
    address_selectors = [
        "#app-root > div > div > div > div:nth-child(5) > div > div:nth-child(2) > div.place_section_content > div > div.O8qbU.tQY7D > div > a > span.LDgIH",
        "#app-root > div > div > div > div:nth-child(5) > div > div:nth-child(2) > div > div > div.O8qbU.tQY7D > div > a > span.LDgIH",
        "#app-root > div > div > div > div:nth-child(5) > div > div.place_section.no_margin > div.place_section_content > div > div.O8qbU.tQY7D > div > a > span.LDgIH",
        # 세 번째 선택자를 추가하세요
    ]

    # 주소 초기화
    address = None

    # 주소를 찾을 때까지 선택자들을 시도
    for address_selector in address_selectors:
        try:
            address_element = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, address_selector))
            )
            address = address_element.text
            break  # 요소를 성공적으로 찾았으면 루프를 종료합니다.
        except Exception as e:
            print(f"선택자를 사용하여 주소를 찾을 수 없습니다: {address_selector}")

    # 평점 확인 및 추출
    grade_selector = ".PXMot.LXIwF"
    grades = driver.find_elements(By.CSS_SELECTOR, grade_selector)
    if grades:
        full_grade_text = grades[0].text
        # 정규 표현식을 사용하여 숫자만 추출합니다.
        grade = re.search(r"\d+(\.\d+)?", full_grade_text).group()
    else:
        grade = 0.00

    image_url = get_image_url(driver)

    # print(
    #     f"인덱스 {index}: 이름: {name}, 유형: {category}, 주소: {address}, 이미지 주소: {image_url}, 평점: {grade}"
    # )

    # 부모 프레임으로 이동
    driver.switch_to.parent_frame()
    # searchIframe로 이동
    search_iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="searchIframe"]'))
    )
    driver.switch_to.frame(search_iframe)

    return name, category, address, image_url, grade


def place_craw(driver, location, category):
    """
    주어진 위치와 카테고리를 기준으로 네이버 플레이스에서 정보 크롤링하고 CSV 파일로 저장합니다.
    """
    remappingValue = industry_remapping(category)
    load_search_results(driver, location, remappingValue)
    number_of_li_elements = find_number_of_li_elements(driver)

    place_info_list = []  # 크롤링한 정보를 저장할 리스트

    for index in range(1, number_of_li_elements + 1):
        place_dic = {}  # 장소 정보를 담을 사전(dictionary)
        place_info = get_place_info(driver, index)
        if place_info:
            place_dic["industry"] = category  # 업종 추가
            place_dic["region"] = location  # 지역명 추가
            place_dic["name"] = place_info[0]
            place_dic["category"] = place_info[1]
            place_dic["address"] = place_info[2]
            place_dic["img_url"] = place_info[3]
            place_dic["grade"] = place_info[4]
            place_info_list.append(place_dic)
        else:
            print(f"{index}. 정보를 가져오는 데 실패했습니다.")

    # 업종 이름을 포함하는 파일 이름 생성
    csv_filename = f"{category.replace('/', '_')}_data.csv"
    save_to_csv(place_info_list, csv_filename)


# # 사용자 입력 예시
# local_of_user2 = "서울시 용산구"
# category_of_user2 = "공연"


def place_other_than_franchises(name, industry):
    industry = industry

    place_other_than_franchises = place_craw(
        name,
        industry,
    )

    # print(place_other_than_franchises)

    return place_other_than_franchises


def industry_remapping(selected_industry):
    # 업종 매핑을 위한 사전 정의
    industry_mapping = {
        "연료": "주유",
        "숙박": "숙박",
        "공연": "공연",
        "렌터카": "렌터카",
        "유흥주점": "유흥주점",
        "레져업소": "레져",
        "자동차유지/정비": "자동차정비",
        "관람(내부)": "관람",
        "관람(외부)": "관람",
        "유통업": "마트",
        "음료/주류": "바",
        "여행/교통": "여행사",
        "오락위락시설": "오락",
        "취미교양용품": "문구",
    }

    # 매핑된 값 찾기, 없을 경우 None 반환
    remapped_industry = industry_mapping.get(selected_industry)

    # 매핑된 값이 없는 경우 에러 발생
    if remapped_industry is None:
        raise ValueError(f"업종명 매핑이 존재하지 않음: {selected_industry}")

    return remapped_industry


def read_json_and_get_names(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
        names = [item["name"] for item in data]
        return names


industry_mapping = {
    "연료": "주유",
    "숙박": "숙박",
    "공연": "공연",
    "렌터카": "렌터카",
    "유흥주점": "유흥주점",
    "레져업소": "레져",
    "자동차유지/정비": "자동차정비",
    "관람(내부)": "관람",
    "관람(외부)": "관람",
    "유통업": "마트",
    "음료/주류": "바",
    "여행/교통": "여행사",
    "오락위락시설": "오락",
    "취미교양용품": "문구",
}

# 업종 리스트 생성
industries = list(industry_mapping.keys())


def main():
    driver = init_driver()
    names = read_json_and_get_names("static/json/regions_coordinates.json")
    start_index_for_names = 0  # Change this to the desired starting index

    for industry in industries:
        index = start_index_for_names

        while index < len(names):
            try:
                name = names[index]
                place_craw(driver, name, industry)
                print(
                    f"Processing: Index = {index}, Industry = {industry}, Region = {name}"
                )
                index += 1  # 다음 인덱스로 이동
            except Exception as e:
                print(f"Error occurred at Index = {index}: {str(e)}")
                # 에러가 발생한 경우 해당 인덱스부터 다시 실행
                continue

    driver.quit()
    print("작업이 끝났습니다.")


# def main():
#     driver = init_driver()
#     names = read_json_and_get_names('static/json/regions_coordinates.json')
#     start_index_for_names = 0  # Change this to the desired starting index
#     industry = "여행/교통"

#     index = start_index_for_names

#     while index < len(names):
#         try:
#             name = names[index]
#             place_craw(driver, name, industry)
#             print(f"Processing: Index = {index}, Industry = {industry}, Region = {name}")
#             index += 1  # 다음 인덱스로 이동
#         except Exception as e:
#             print(f"Error occurred at Index = {index}: {str(e)}")
#             # 에러가 발생한 경우 해당 인덱스부터 다시 실행
#             continue

#     driver.quit()
#     print("작업이 끝났습니다.")

if __name__ == "__main__":
    main()
