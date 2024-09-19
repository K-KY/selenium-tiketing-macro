from contextlib import nullcontext

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from seleniumMacro.OpenAiConnector import connect_open_ai
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time

class SeatFinder:

    @staticmethod
    def find(area, driver) :
        print("----------find---------")
        for li in area:
            try:
                print("탐색", li.text)
                if "(0석)" in li.text:
                    print("좌석이 없으므로 다음 구역 탐색...")
                    continue  # 조건을 만족한 경우 다음 반복으로 넘어감

                li.click()
                # title 속성이 있고 문자열 길이가 0보다 큰 요소를 찾기
                target = (
                    driver
                    .find_element(
                        By.XPATH, '//*[@id="divSeatArray"]/div[string-length(@title)>0 and not(contains(@class, "s13"))]'))
                print(f"찾은 요소: {target.text}")
                # 원하는 작업 수행 (예: 클릭)
                return target
            except NoSuchElementException:
                # 요소를 찾지 못했을 때
                print("요소를 찾지 못했습니다. 다시 시도 중...")
                # 다시 루프를 반복하여 요소를 찾기


