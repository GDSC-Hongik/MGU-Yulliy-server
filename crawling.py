# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pandas as pd

# 페이지 로딩을 기다리는데 사용할 time 모듈 import
import time

# 크롬드라이버 실행
driver = webdriver.Chrome()

# 크롬 드라이버에 url 주소 넣고 실행
driver.get("https://map.kakao.com/")

# 페이지가 완전히 로딩되도록 4초 동안 기다림
time.sleep(4)


def get_lag_lng(address):
    # 검색어 창을 찾아 search_box 변수에 저장 (By.ID 방식)
    search_box = driver.find_element(By.ID, "addr")
    # 검색하기 버튼을 찾아 enter_box 변수에 저장
    enter_box = driver.find_element(By.CLASS_NAME, "btn.h22")

    # 다른 값이 들어오면 필터링
    if type(address) is not str:
        return "좌표가 검색 되지 않았습니다", "좌표가 검색되지 않았습니다"

    search = address.split("\n", 1)[0]
    search_box.send_keys(search)
    enter_box.click()
    time.sleep(2)

    try:
        # 위도 경도 찾아서 변수에 넣기
        laglng = driver.find_element(By.ID, "coord")
        # 위도, 공백, 경도 분리하여 변수에 지정
        lag, _, lng = laglng.text.split("\n")
    except Exception:
        driver.refresh()
        return "좌표가 검색 되지 않았습니다", "좌표가 검색되지 않았습니다"

    try:
        lagtitude = lag.split(":")[1]  # 위도 : __._______
    except Exception:
        lagtitude = "NULL"
    try:
        longitude = lng.split(":")[1]  # 경도 : __._______
    except Exception:
        longitude = "NULL"

    time.sleep(1)

    # 검색어 창 비우기(새로고침)
    driver.refresh()

    return lagtitude, longitude


def get_type(restaurant_name):
    search_box = driver.find_element(By.ID, "search.keyword.query")
    search_box.send_keys(restaurant_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    try:
        rtype = driver.find_element(By.CLASS_NAME, "subcategory")
        type = rtype.text
    except Exception:
        type = "null"

    time.sleep(1)

    # 검색어 창 비우기
    search_box.clear()

    return type


# Load the CSV file
file_path = "final.csv"
data = pd.read_csv(file_path)

# 칼럼 추가
data["Type"] = None

# 식당으로 타입 획득 후 입력
for index, row in data.iterrows():
    restaurant_address = row["Name"]
    type = get_type(restaurant_address)
    data.at[index, "Type"] = type
    time.sleep(1)

# 데이터 저장
data.to_csv("restauranttype.csv", encoding="utf-8-sig", index=False)

# 브라우저 닫기
driver.quit()
