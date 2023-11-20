from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


def init_driver():
    """
    웹 드라이버 초기화 및 옵션 설정
    """
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def load_search_results(driver, location, category):
    """
    주어진 위치와 카테고리로 네이버 플레이스 검색 결과 페이지 로드
    """
    search_url = f"https://map.naver.com/p/search/{location} {category}"
    driver.get(search_url)
    time.sleep(5)  # 페이지 로딩 대기


def load_place_filter(
    driver, general_preference, ambiance_preference_option1, ambiance_preference_option2
):
    """
    플레이스 필터 적용
    """
    # iframe 전환
    search_iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="searchIframe"]'))
    )
    driver.switch_to.frame(search_iframe)

    # 플레이스 필터를 클릭
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app-root"]/div/div[1]/div/div/div/div/div/span[1]/a')
        )
    ).click()

    time.sleep(1)

    # 정렬속성 선택
    if general_preference == "많이찾는":
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="_place_portal_root"]/div/div[2]/div[1]/div/div/div[1]/div[2]/a[1]',
                )
            )
        ).click()

    elif general_preference == "요즘뜨는":
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="_place_portal_root"]/div/div[2]/div[1]/div/div/div[1]/div[2]/a[2]',
                )
            )
        ).click()

    elif general_preference == "리뷰많은":
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="_place_portal_root"]/div/div[2]/div[1]/div/div/div[1]/div[2]/a[5]',
                )
            )
        ).click()

    # 분위기 선택
    if ambiance_preference_option1 == "조용한" or ambiance_preference_option2 == "조용한":
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="_place_portal_root"]/div/div[2]/div[1]/div/div/div[7]/div[2]/a[1]',
                )
            )
        ).click()

    if ambiance_preference_option1 == "분위기좋은" or ambiance_preference_option2 == "분위기좋은":
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="_place_portal_root"]/div/div[2]/div[1]/div/div/div[7]/div[2]/a[2]',
                )
            )
        ).click()

    # 플레이스 필터 적용 버튼 클릭
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="_place_portal_root"]/div/div[2]/div[2]/a[2]')
        )
    ).click()

    # 필터를 누르고 페이지가 로딩될때까지 몇초정도 기다려야함.
    time.sleep(2)


def get_restaurant_info(driver, index):
    """
    주어진 인덱스에 해당하는 음식점 정보 추출
    """
    # 음식점 클릭
    try:
        restaurant_selector = f"#_pcmap_list_scroll_container > ul > li:nth-child({index}) > div.CHC5F > a.tzwk0 > div > div > span.TYaxT"
        restaurant_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, restaurant_selector))
        )
        actions = driver.find_element(By.CSS_SELECTOR, "body")
        actions.send_keys(Keys.END)
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

    # 가게 이름, 유형, 주소 추출
    name = (
        WebDriverWait(driver, 1)
        .until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#_title > span.Fc1rA"))
        )
        .text
    )

    category = (
        WebDriverWait(driver, 1)
        .until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#_title > span.DJJvD"))
        )
        .text
    )

    address = (
        WebDriverWait(driver, 1)
        .until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#app-root > div > div > div > div:nth-child(5) > div > div:nth-child(2) > div.place_section_content > div > div.O8qbU.tQY7D > div > a > span.LDgIH",
                )
            )
        )
        .text
    )

    # 부모 프레임으로 이동
    driver.switch_to.parent_frame()
    search_iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="searchIframe"]'))
    )
    driver.switch_to.frame(search_iframe)

    return name, category, address


def eat_craw(
    location,
    category,
    general_preference,
    ambiance_preference_option1,
    ambiance_preference_option2,
):
    """
    주어진 위치와 카테고리를 기준으로 네이버 플레이스에서 음식점 정보 크롤링
    """
    driver = init_driver()
    load_search_results(driver, location, category)
    load_place_filter(
        driver,
        general_preference,
        ambiance_preference_option1,
        ambiance_preference_option2,
    )

    # 크롤링한 정보를 저장할 리스트
    restaurants_info_list = []

    for index in range(1, 10):
        # 식당 정보를 담을 사전(dictionary) 생성
        restaurant_dic = {}

        restaurant_info = get_restaurant_info(driver, index)
        if restaurant_info:
            restaurant_dic["res_name"] = restaurant_info[0]
            restaurant_dic["res_category"] = restaurant_info[1]
            restaurant_dic["res_address"] = restaurant_info[2]
            restaurants_info_list.append(restaurant_dic)
        else:
            print(f"{index}. 정보를 가져오는 데 실패했습니다.")
            continue

    # 드라이버 종료 코드 (필요한 경우 주석 해제)
    # driver.quit()

    return restaurants_info_list


# 사용자 입력 예시
local_of_user2 = "서울시 용산구"
category_of_user2 = "일식"
general_preference_of_user2 = "많이찾는"
ambiance_preference_option1_of_user2 = "조용한"
ambiance_preference_option2_of_user2 = "분위기좋은"


def franchises():
    franchises = eat_craw(
        local_of_user2,
        category_of_user2,
        general_preference_of_user2,
        ambiance_preference_option1_of_user2,
        ambiance_preference_option2_of_user2,
    )
    return franchises
